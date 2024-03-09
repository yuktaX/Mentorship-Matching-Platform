from flask import Flask,render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import smtplib


 
app = Flask(__name__)
#from app import routes, models
 
app.secret_key = 'your secret key'


 
 
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '281613'
app.config['MYSQL_DB'] = 'mentify'
 
 
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

    server.login(sender,passcode)               # dummy passcode. Sender should be your email id. passcode is app password. Explained in detail in readme file
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
                return redirect(url_for("dashboard"))
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

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/user_category',methods=['GET','POST'])
def user_category():
    global user_type
    user_type=request.form['button']
    print("User type : ", user_type)   
    return render_template("signup.html",user_type=user_type)


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
            #qualification=request.form['qualification']
           # work_exp=request.form['work_exp']
            cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
           'INSERT INTO mentor(mentor_name,contact_no,email_id,username,pass_word) VALUES(%s, %s, %s,%s, %s)', (name,contact_no,email_id,username,password) )
            mysql.connection.commit()
            send_email("mentify@example.com",email_id,"Thanks for joining Mentify","Welcome to Mentify! You have successfully signed up as a mentor on Mentify! Kindly log into Mentify website and upload your resume. On approval by admin you will be able to create courses and enroll mentees. On aproval you will be sent a confirmation email")  #Replace mentify@example.com with your email_id
            return render_template("login.html",msg="Signup Successful. You may login Now")

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('landing'))

if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)
            
 