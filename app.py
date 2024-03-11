from flask import Flask,render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import smtplib
import os
from werkzeug.utils import secure_filename
import random


 
app = Flask(__name__)
#from app import routes, models
 
app.secret_key = 'your secret key'


 
 
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '281613'
app.config['MYSQL_DB'] = 'mentify'
app.config['UPLOAD_FOLDER']='F:\\de shaw\\project2\\Mentorship-Matching-Platform\\file_uploads'  #provide folder path here where to store resumes
 
 
mysql = MySQL(app)

user_type=''

def init_db():
    with app.app_context():
        db = mysql.connection
        with app.open_resource('schema.sql', mode='r') as f:
            sql_commands = f.read().split(';')
            cursor = db.cursor()
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)
        db.commit()

def send_email(sender,receiver,subject,message):
    passcode=''
    text=f"Subject : {subject}\n\n{message}"
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()

    server.login(sender,"xxxxxxxxxxxxxx")               # dummy passcode. Sender should be your email id. passcode is app password. Explained in detail in readme file
    server.sendmail(sender,receiver,text)
    print("Email has been sent to : ", receiver)


@app.route('/')
def hello():
    return render_template('landing.html')
@app.route('/login')
def hello2():
    return render_template('login.html')

@app.route('/process_login',methods=['GET','POST'])
def process_login():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username=request.form['username']
        password=request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM mentee WHERE username = % s ', (username,) )
        user=cursor.fetchone()
        if user:
    
            if user['pass_word'] == request.form.get("password"):
                session['loggedin']=True
                return redirect(url_for("dashboard_mentee",username=username))
            else:                
                msg="incorrect username or password"
                return render_template("login.html",msg=msg)
        else:
            cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
            'SELECT * FROM mentor WHERE username = % s ', (username,) )
            user=cursor.fetchone()
            if user:
                if user['pass_word'] == request.form.get("password"):
                    session['loggedin']=True
                    return redirect(url_for("dashboard"))
            else:
                msg="incorrect username or password"
                return render_template("login.html",msg=msg)
            
    # return render_template('login.html')
        
#@app.route('\signup_process',methods=['GET','POST'])
#def signup_process():
 #   msg=''
  #  if request.method=='POST'and 'Full name' in request.form and 'Email address' in request.form and 'Phone number' in request.form  and 


@app.route('/signup_main',methods=['GET','POST'])
def signup_main():
    return render_template("signup_main.html")

@app.route('/dashboard_mentee/<username>')
def dashboard_mentee(username):
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
            'SELECT * FROM mentee WHERE username = % s ', (username,) )
    mentee=cursor.fetchone()
    print(mentee)
    mentee_name=mentee['mentee_name']
    return render_template("dashboard_mentee.html",mentee=mentee_name,username=mentee['username'])

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard_mentee.html")

@app.route('/user_category',methods=['GET','POST'])
def user_category():
    global user_type
    user_type=request.form['button']
    print("User type : ", user_type)
    if(user_type=='mentee'):   
        return render_template("signup_mentee.html")
    elif(user_type=='mentor'):
        return render_template("signup_mentor.html")

@app.route('/profile_mentee/<username>',methods=['GET','POST'])
def profile_mentee(username):
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
            'SELECT * FROM mentee WHERE username = % s ', (username,) )
    mentee=cursor.fetchone()
    if request.method=='POST':
        new_name=request.form['name']
        new_contact=request.form['contact_no']
        new_email=request.form['email_id']
        new_education=request.form['education']
        new_interest=request.form['interests']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE mentee SET mentee_name = %s,contact_no=%s,email_id=%s,education=%s,interests=%s WHERE username = %s',(new_name,new_contact,new_email,new_education,new_interest,username))
        mysql.connection.commit()
        return render_template('profile_mentee.html',name=new_name,username=username,contact_no=new_contact,email_id=new_email,education=new_education,interests=new_interest,msg='Profile details updated successfully')

    return render_template('profile_mentee.html',name=mentee['mentee_name'],username=mentee['username'],contact_no=mentee['contact_no'],email_id=mentee['email_id'],education=mentee['education'],interests=mentee['interests'],msg='')


@app.route('/signup',methods=['GET','POST'])
def signup_process():
    
    msg=''
    if request.method=='POST':
        print(user_type)
        if user_type=="mentee": 
            print("registering mentee")
            name = request.form['name']
            contact_no = request.form['contact_no']
            email_id = request.form['email']
            password = request.form['password']
            username = request.form['username']
            cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
            'INSERT INTO mentee(mentee_name,contact_no,email_id,username,pass_word) VALUES(%s,%s, %s,%s, %s)', (name,contact_no,email_id,username,password) )
            mysql.connection.commit()
            send_email("mentify@example.com",email_id,"Thanks for joining Mentify","Welcome to Mentify! You have successfully signed up as a mentee on Mentify!")       #Replace mentify@example.com with your email_id
            return render_template("login.html",msg="Signup Successful. You may login Now")
        else:
            print("registering mentor")
            name = request.form['name']
            contact_no = request.form['contact_no']
            email_id = request.form['email']
            password = request.form['password']
            username = request.form['username']
            resume=request.files['file']
            if resume:
                filename = secure_filename(resume.filename)
                resume.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print('File uploaded successfully')
            #qualification=request.form['qualification']
           # work_exp=request.form['work_exp']
            cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
           'INSERT INTO mentor(mentor_name,contact_no,email_id,username,pass_word,file_name) VALUES(%s, %s, %s,%s, %s,%s)', (name,contact_no,email_id,username,password,resume.filename) )
            mysql.connection.commit()
            send_email("mentify@example.com",email_id,"Thanks for joining Mentify","Welcome to Mentify! You have successfully signed up as a mentor on Mentify! Kindly log into Mentify website and upload your resume. On approval by admin you will be able to create courses and enroll mentees. On aproval you will be sent a confirmation email")  #Replace mentify@example.com with your email_id
            return render_template("login.html",msg="Signup Successful. You may login Now")
        
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    global otp_gen
    global email_fp
    global usertype_fp
    if request.method == 'POST':
        if 'username' in request.form and 'email' in request.form:
            username = request.form['username']
            email_fp = request.form['email']
            cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
            'SELECT * FROM mentee WHERE username = % s ', (username,) )
            user=cursor.fetchone()
            if user:
                usertype_fp='mentee'
                if(email_fp==user['email_id']):
                    otp = str(random.randint(100000, 999999))
                    otp_gen=otp
                    send_email("mentify@example.com",email_fp,"OTP For Changing Password",f"Hi {user['mentee_name']}!\nOTP for changing password is {otp}. Do not share the OTP with anyone.\nIf you did not apply for changing password kindly report it on Mentify website.")
                    return render_template('forgot_password.html', username=username, show_otp_form=True,msg='')
                else:
                    return render_template('forgot_password.html', username=username, show_otp_form=False,msg='Incorrect Email Id entered')
            else:
                cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(
                    'SELECT * FROM mentor WHERE username = % s ', (username,) )
                user=cursor.fetchone()
                if user:
                    usertype_fp='mentor'
                    if(email_fp==user['email_id']):
                        otp = str(random.randint(100000, 999999))
                        otp_gen=otp
                        send_email("mentify@example.com",email_fp,"OTP For Changing Password",f"Hi {user['mentor_name']}!\nOTP for changing password is {otp}. Do not share the OTP with anyone.\nIf you did not apply for changing password kindly report it on Mentify website.")
                        return render_template('forgot_password.html', username=username, show_otp_form=True,msg='')
                    else:
                        return render_template('forgot_password.html', username=username, show_otp_form=False,msg='Incorrect Email Id entered')                   
                else:
                    return render_template('forgot_password.html', username=username, show_otp_form=False,msg='Incorrect username entered')

        elif 'otp' in request.form and 'new_password' in request.form:
            username = request.form['username']
            otp_entered = request.form['otp']
            new_password = request.form['new_password']
            print(f"Otp gen : {otp_gen}, otp_entered : {otp_entered}")
            if(otp_entered==otp_gen):
                send_email("mentify@example.com",email_fp,"Password Changed","Greetings from Mentify! Password of your mentify account has been successfully changed! If you did not initiate the password change, kindly contact mentify support team.")
                cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                if(usertype_fp=='mentee'):
                    cursor.execute('UPDATE mentee SET pass_word = %s WHERE username = %s AND email_id = %s',(new_password,username,email_fp))
                elif(usertype_fp=='mentor'):
                    cursor.execute('UPDATE mentor SET pass_word = %s WHERE username = %s AND email_id = %s',(new_password,username,email_fp))
                mysql.connection.commit()
                return render_template('login.html',msg="Password change successful!")
            else:
                return render_template('forgot_password.html', username=username, show_otp_form=False,msg='Incorrect OTP entered')
            

    # Render the default form for entering username and email
    return render_template('forgot_password.html', show_otp_form=False,msg='')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('hello'))

if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)
            
 