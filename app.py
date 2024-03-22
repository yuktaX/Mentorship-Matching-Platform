from flask import Flask,render_template, request, redirect, url_for, session,send_file
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import smtplib
import os
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit
import random
from datetime import datetime
#import search_and_filter.py

 
app = Flask(__name__)
#from app import routes, models
 
app.secret_key = 'your secret key'


 
 
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '281613'
app.config['MYSQL_DB'] = 'mentify'
app.config['UPLOAD_FOLDER']='F:\\de shaw\\project2\\Mentorship-Matching-Platform\\file_uploads'  #provide folder path here where to store resumes
 
 
mysql = MySQL(app)
socketio = SocketIO(app)

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

    server.login(sender,"xxxxxxxxxxxx")               # dummy passcode. Sender should be your email id. passcode is app password. Explained in detail in readme file
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
                    return redirect(url_for("dashboard_mentor",username=username))
            else:
                msg="incorrect username or password"
                return render_template("login.html",msg=msg)
            


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

    cursor.execute('SELECT * FROM tag')  
    tags = cursor.fetchall()
    return render_template("dashboard_mentee.html",mentee=mentee_name,username=mentee['username'],tags=tags,selected_filter = 'none')

@app.route('/dashboard_mentor/<username>')
def dashboard_mentor(username):
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
            'SELECT * FROM mentor WHERE username = % s ', (username,) )
    mentor=cursor.fetchone()
    cursor.execute(
            'SELECT * FROM course WHERE mentor_id = % s ', (mentor['mentor_id'],) )
    courses=cursor.fetchall()
    return render_template("dashboard_mentor.html",mentor=mentor,username=mentor['username'],courses=courses)



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
            send_email("vaishnoviarun7060@gmail.com",email_id,"Thanks for joining Mentify","Welcome to Mentify! You have successfully signed up as a mentee on Mentify!")       #Replace mentify@example.com with your email_id
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
                print("Filename : ",filename )
                os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], username), exist_ok=True)
                resume.save(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], username), filename))
                print('File uploaded successfully')
            #qualification=request.form['qualification']
           # work_exp=request.form['work_exp']
            cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
           'INSERT INTO mentor(mentor_name,contact_no,email_id,username,pass_word,file_name,mentor_status) VALUES(%s, %s, %s,%s, %s,%s,%s)', (name,contact_no,email_id,username,password,resume.filename,'unverified') )
            mysql.connection.commit()
            send_email("vaishnoviarun7060@gmail.com",email_id,"Thanks for joining Mentify","Welcome to Mentify! You have successfully signed up as a mentor on Mentify! Kindly log into Mentify website and upload your resume. On approval by admin you will be able to create courses and enroll mentees. On aproval you will be sent a confirmation email")  #Replace mentify@example.com with your email_id
            return render_template("login.html",msg="Signup Successful. You may login Now")


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
    cursor.execute('SELECT * FROM tag')
    all_tags=cursor.fetchall()
    cursor.execute('SELECT * FROM mentee_tag WHERE mentee_id=%s',(mentee['mentee_id'],))
    mentee_tags=cursor.fetchall()
    print("Mentee tags : ",mentee_tags)
    is_checked={}
    for tag in mentee_tags:
        print('tag : ',tag)
        print(f"tag_id : {tag['tag_id']}")
        cursor.execute('SELECT * FROM tag WHERE tag_id = %s',(tag['tag_id'],))
        tag_val=cursor.fetchone()
        tag_name=tag_val['tag_name']
        is_checked[tag_name]=1

    if request.method=='POST':
        new_name=request.form['name']
        new_contact=request.form['contact_no']
        new_email=request.form['email_id']
        new_education=request.form['education']
        new_interest=request.form['interests']
        cursor.execute('DELETE FROM mentee_tag WHERE mentee_id = %s', (mentee['mentee_id'],))
        mysql.connection.commit()
        new_checked={}
        for tag in all_tags:
            tag_name=tag['tag_name']
            
            tag_id=tag['tag_id']
            if tag_name in request.form:
                new_checked[tag_name]=1
                cursor.execute('INSERT INTO mentee_tag(mentee_id,tag_id) VALUES (%s,%s)',(mentee['mentee_id'],tag_id))
                mysql.connection.commit()
    
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE mentee SET mentee_name = %s,contact_no=%s,email_id=%s,education=%s,interests=%s WHERE username = %s',(new_name,new_contact,new_email,new_education,new_interest,username))
    
        mysql.connection.commit()
        return render_template('profile_mentee.html',name=new_name,username=username,contact_no=new_contact,email_id=new_email,education=new_education,interests=new_interest,msg='Profile details updated successfully',tags=all_tags,is_checked=new_checked)

    return render_template('profile_mentee.html',name=mentee['mentee_name'],username=mentee['username'],contact_no=mentee['contact_no'],email_id=mentee['email_id'],education=mentee['education'],interests=mentee['interests'],msg='',tags=all_tags,is_checked=is_checked)

@app.route('/profile_mentor/<username>',methods=['GET','POST'])
def profile_mentor(username):
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
            'SELECT * FROM mentor WHERE username = % s ', (username,) )
    mentor=cursor.fetchone()
    if request.method=='POST':
        new_name=request.form['name']
        new_contact=request.form['contact_no']
        new_email=request.form['email_id']
        new_institute=request.form['education']
        new_degree=request.form['degree']
        new_major=request.form['major']
        new_workexp=request.form['work_exp']
        new_interest=request.form['interests']
        new_file=request.files['file']
        if new_file:
                file_path = os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], username),mentor['file_name'])
                if os.path.exists(file_path):
                    os.unlink(file_path)
                filename = secure_filename(new_file.filename)
                print("Filename : ",filename )
                os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], username), exist_ok=True)
                new_file.save(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], username), filename))
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE mentor SET mentor_name = %s,contact_no=%s,email_id=%s,institute=%s,degree=%s,major=%s,work_exp=%s,interests=%s,file_name = %s WHERE username = %s',(new_name,new_contact,new_email,new_institute,new_degree,new_major,new_workexp,new_interest,filename,username))
        mysql.connection.commit()
        return render_template('profile_mentor.html',name=new_name,username=username,contact_no=new_contact,email_id=new_email,education=new_institute,degree=new_degree,major=new_major,work_exp=new_workexp,interests=new_interest,msg='Profile details updated successfully',view_profile=False,give_approval=False)

    return render_template('profile_mentor.html',name=mentor['mentor_name'],username=mentor['username'],contact_no=mentor['contact_no'],email_id=mentor['email_id'],education=mentor['institute'],degree=mentor['degree'],major=mentor['major'],work_exp=mentor['work_exp'],interests=mentor['interests'],msg='',view_profile=False,give_approval=False)

@app.route('/view_file/<username>/<filename>')
def view_file(username, filename):
    file_path=os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], username), filename)
    return send_file(file_path, as_attachment=True)

@app.route('/view_mentor_profile',methods=['GET','POST'])
def view_mentor_profile():
    viewer = request.args.get('viewer')
    username=request.args.get('username')
   
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
            'SELECT * FROM mentor WHERE username = % s ', (username,) )
    mentor=cursor.fetchone()
    
    if request.method=='POST':
        if 'accept' in request.form:
            cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE mentor SET mentor_status = %s WHERE username = %s' ,('verified',username) )
            mysql.connection.commit()
            send_email("vaishnoviarun7060@gmail.com",mentor['email_id'],"Approval for Mentorship","Greetings from Mentify! Your profile has been verified by Mentify. Now you can log into our website and create courses, hold mentorship sessions and much more! Welcome onboard!")
        elif 'reject' in request.form:
            cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE mentor SET mentor_status = %s WHERE username = %s' ,('rejected',username) )
            mysql.connection.commit()
            send_email("vaishnoviarun7060@gmail.com",mentor['email_id'],"Application status for Mentorship","Greetings from Mentify! Your profile has been inspected by Mentify. We regret to inform you that we could not ascertain your application. Please log into our website to update your profile details so that we may inspect it again. ")
        return redirect(url_for('admin'))
    return render_template('profile_mentor.html',mentor=mentor,name=mentor['mentor_name'],username=mentor['username'],contact_no=mentor['contact_no'],email_id=mentor['email_id'],degree=mentor['degree'],education=mentor['institute'],major=mentor['major'],work_exp=mentor['work_exp'],interests=mentor['interests'],msg='',view_profile=True,give_approval=True,filename=mentor['file_name'],viewer=viewer)
    
@app.route('/create_program/<username>',methods=['GET','POST'])
def create_program(username):
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM tag')
    tags=cursor.fetchall()
    cursor.execute('SELECT mentor_id FROM mentor WHERE username=%s',(username,))
    mentor_id=cursor.fetchone()
    
    if request.method=='POST':
        course_name=request.form['course_name']
        start_date=request.form['start_date']
        end_date=request.form['end_date']
        price=request.form['price']
        mentor_id=mentor_id['mentor_id']
        course_desc=request.form['desc']
        max_mentee=request.form['max_mentee']
        print(mentor_id)
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO course(mentor_id, course_name, course_start, course_end, course_price,course_status,course_desc,max_limit) VALUES (%s, %s, %s, %s, %s,%s,%s,%s)', (mentor_id, course_name, start_date, end_date, price,'unverified',course_desc,max_mentee))
        mysql.connection.commit()
        cursor.execute('SELECT * FROM course WHERE course_name = %s',(course_name,))
        course=cursor.fetchone()
        print(course)
        course_id=course['course_id']
        for tag in tags:
            tag_name=tag['tag_name']
            tag_id=tag['tag_id']
            if tag_name in request.form:
                cursor.execute('INSERT INTO course_tag_relation(course_id,tag_id) VALUES(%s,%s)',(course_id,tag_id))
        mysql.connection.commit()
        return render_template('create_program_mentor.html',username=username,tags=tags,msg='Course proposal successfully submitted. On approval by Mentify, you will receive an email confirming acceptance of your proposal and mentees will be able to join your program ')
    return render_template('create_program_mentor.html',username=username,tags=tags,msg='')


        
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
                    send_email("vaishnoviarun7060@gmail.com",email_fp,"OTP For Changing Password",f"Hi {user['mentee_name']}!\nOTP for changing password is {otp}. Do not share the OTP with anyone.\nIf you did not apply for changing password kindly report it on Mentify website.")
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
                        send_email("vaishnoviarun7060@gmail.com",email_fp,"OTP For Changing Password",f"Hi {user['mentor_name']}!\nOTP for changing password is {otp}. Do not share the OTP with anyone.\nIf you did not apply for changing password kindly report it on Mentify website.")
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
                send_email("vaishnoviarun7060@gmail.com",email_fp,"Password Changed","Greetings from Mentify! Password of your mentify account has been successfully changed! If you did not initiate the password change, kindly contact mentify support team.")
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

@app.route('/admin',methods=['GET','POST'])
def admin():
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM mentor WHERE mentor_status = %s', ('unverified',))
    unapproved_mentors=cursor.fetchall()
    cursor.execute('SELECT * FROM course WHERE course_status = %s', ('unverified',))
    unapproved_courses=cursor.fetchall()
    cursor.execute("SELECT * FROM mentee_complaints WHERE complaint_status='pending'")
    mentee_pending_complaints = cursor.fetchall()
    cursor.execute("SELECT * FROM mentor_complaints WHERE complaint_status='pending'")
    mentor_pending_complaints = cursor.fetchall()
    return render_template("admin.html",mentors=unapproved_mentors,courses=unapproved_courses,mentee_complaints=mentee_pending_complaints,mentor_complaints=mentor_pending_complaints)

@app.route('/add_tag',methods=['GET','POST'])
def add_tag():       
    if request.method=='POST':
        new_tag=request.form['tag']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tag WHERE tag_name=%s',(new_tag,))
        existing_tag=cursor.fetchone()
        if not existing_tag:
            cursor.execute('INSERT INTO tag(tag_name) VALUES (%s)', (new_tag,))
            mysql.connection.commit()
        return redirect(url_for('admin'))

@app.route('/view_course',methods=['GET','POST'])
def view_course():
    viewer = request.args.get('viewer')
    course_id = int(request.args.get('course_id'))
    mentee_id=int(request.args.get('mentee_id'))

    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM course WHERE course_id = %s', (course_id,))
    course=cursor.fetchone()
    cursor.execute('SELECT * FROM mentor WHERE mentor_id = %s', (course['mentor_id'],))
    mentor=cursor.fetchone()
    cursor.execute('SELECT * FROM course_tag_relation WHERE course_id=%s',(course['course_id'],))
    tag_rel=cursor.fetchall()
    tags=[]
    for tag in tag_rel:
        cursor.execute('SELECT * FROM tag WHERE tag_id=%s',(tag['tag_id'],))
        tag_new=cursor.fetchone()
        tags.append(tag_new)
    if viewer=='admin':
        return render_template('view_course.html',course=course,viewer=viewer,mentor=mentor,tags=tags,mentee_id=0)
    elif viewer=='mentee':
        if not mentee_id==0:
            return render_template('view_course.html',course=course,viewer=viewer,mentor=mentor,tags=tags,mentee_id=mentee_id)
    elif viewer=='mentor':
        return render_template('view_course.html',course=course,viewer=viewer,mentor=mentor,tags=tags,mentee_id=0)

    return render_template('view_course.html',course=course,viewer=viewer,mentor=mentor,tags=tags,mentee_id=0)


@app.route('/process_viewer_request',methods=['GET','POST'])
def process_viewer_request():
    course_id=int(request.args.get('course_id'))
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method=='POST':
        if 'admin_comment' in request.form:
            admin_comment=request.form['admin_comment']
            print(admin_comment)
            if 'accept' in request.form:
                cursor.execute('UPDATE course SET admin_comment= %s,course_status=%s WHERE course_id=%s',(admin_comment,'verified',course_id))
                mysql.connection.commit()
            elif 'reject' in request.form:
                cursor.execute('UPDATE course SET admin_comment=%s AND course_status=%s WHERE course_id=%s',(admin_comment,'rejected',course_id))
                mysql.connection.commit()
            return redirect(url_for('admin'))
        elif 'register' in request.form:
            amount=request.form['price']
            return redirect(url_for('payment',+ f'?amount={amount}&course_id={course_id}'))

@app.route('/payment',methods=['GET','POST'])
def payment():
    amount = request.args.get('amount')
    mentee_id = int(request.args.get('mentee_id'))
    course_id=int(request.args.get('course_id'))
    if request.method=='POST':
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO course_mentee(mentee_id,course_id) VALUES(%s,%s)',(mentee_id,course_id))
        mysql.connection.commit()
        cursor.execute('SELECT * FROM mentee WHERE mentee_id=%s',(mentee_id,))
        mentee=cursor.fetchone()
        cursor.execute('SELECT * FROM course WHERE course_id=%s',(course_id,))
        course=cursor.fetchone()
        cursor.execute('SELECT * FROM mentor WHERE mentor_id=%s',(course['mentor_id'],))
        mentor=cursor.fetchone()
        send_email("vaishnoviarun7060@gmail.com",mentee['email_id'],"Course registration successful",f"Dear {mentee['mentee_name']}, you have successfully registered for the course {course['course_name']} conducted by mentor {mentor['mentor_name']}.\n Login to your Mentify account to check out course details!")
        send_email("vaishnoviarun7060@gmail.com",mentor['email_id'],"Course registration",f"Dear {mentor['mentor_name']}, Mentee {mentee['mentee_name']} has enrolled for your course {course['course_name']}. You may now mentor your mentee and help him/her achieve their goals!!Login to your mentify account!!")
        return redirect(url_for('dashboard_mentee',username=mentee['username']))
    

    return render_template('payment.html',amount=amount)             

@app.route('/submit_mentee_complaint/<int:mentee_id>', methods=['GET','POST'])
def submit_mentee_complaint(mentee_id):
    if request.method=='POST':
        complaint_date = datetime.now()
        complaint_desc = request.form['complaint_desc']    
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO mentee_complaints (mentee_id, complaint_date, complaint_desc) VALUES (%s, %s, %s)", (mentee_id, complaint_date, complaint_desc))
        mysql.connection.commit()
        cursor.execute("SELECT * FROM mentee WHERE mentee_id=%s",(mentee_id,))
        mentee=cursor.fetchone()
        send_email("vaishnoviarun7060@gmail.com",mentee['email_id'],"Complaint registered successfully",f"Dear {mentee['mentee_name']},your complaint has been registered successfully.\nYou may check the status of the complaint on our website.")
        return render_template('raise_ticket.html',msg='Complaint successfully submitted')
        
    return render_template('raise_ticket.html',msg='')

@app.route('/submit_mentor_complaint/<int:mentor_id>', methods=['GET','POST'])
def submit_mentor_complaint(mentor_id):
    if request.method=='POST':
        complaint_date = datetime.now()
        complaint_desc = request.form['complaint_desc']    
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO mentor_complaints (mentor_id, complaint_date, complaint_desc) VALUES (%s, %s, %s)", (mentor_id, complaint_date, complaint_desc))
        mysql.connection.commit()
        cursor.execute("SELECT * FROM mentor WHERE mentor_id=%s",(mentor_id,))
        mentor=cursor.fetchone()
        send_email("vaishnoviarun7060@gmail.com",mentor['email_id'],"Complaint registered successfully",f"Dear {mentor['mentor_name']},your complaint has been registered successfully.\nYou may check the status of the complaint on our website.")
        return render_template('raise_ticket.html',msg='Complaint successfully submitted')
        
    return render_template('raise_ticket.html',msg='')

@app.route('/messages/<course_name>/<username>')
def messages(course_name,username):
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM messages where course_name = %s',(course_name,))
        messages = cursor.fetchall()
        return render_template('my_courses_page_mentee.html',course_name=course_name,username=username,messages=messages)

@app.route('/search_sort_filter', methods=['POST'])
def search_sort_filter():
    """Sorts, searches, and filters data based on the provided parameters."""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM tag')
    tag = cursor.fetchall()

    parameters = []
    sort_option = "no_of_registrations DESC"
    query = "SELECT course.*, mentor.mentor_name FROM course JOIN mentor ON course.mentor_id = mentor.mentor_id"
    sort_choice = request.form['sort']

    if 'sort' in request.form:
        if sort_choice == 'valuation':
            sort_option = "no_of_registrations DESC"
        elif sort_choice == 'equity':
            sort_option = "course_price ASC"
        elif sort_choice == 'investment':
            sort_option = "course_price DESC"

    selected_tag = request.form['filter']
    if 'filter' in request.form:
        print("tag : ", selected_tag)
        if selected_tag != 'none':
            query += " JOIN course_tag_relation ON course.course_id = course_tag_relation.course_id"
            query += " JOIN tag ON course_tag_relation.tag_id = tag.tag_id"
            query += " WHERE tag.tag_name = %s"
            parameters.append(selected_tag)
    else:
        query += " WHERE 1=1"  # Ensuring the WHERE clause is present even if no tag is selected

    search_term = request.form.get('search_term')
    search_type = request.form.get('search_type')

    if search_term:
        print("Search Term:", search_term)
        print("Search Type:", search_type)

        if search_type == 'mentor':
            query += " AND mentor.mentor_name LIKE %s"
        elif search_type == 'course':
            query += " AND course.course_name LIKE %s"
        parameters.append("%" + search_term + "%")

    query += f" ORDER BY {sort_option}"

    cursor.execute(query, parameters)

    print("Final query:", query)
    print("Parameters:", parameters)
    print(selected_tag)
    cursor.execute(query, parameters)
    data = cursor.fetchall()
    # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    #     return jsonify(data=data,tag=tag)  # Return JSON response for AJAX request
    # else:
    return render_template('dashboard_mentee.html', data=data, tags=tag, selected_filter=selected_tag, sort_option=sort_choice, search_term=search_term, search_type=search_type)
 
@socketio.on('new_message')
def handle_new_message(data):
    sender = data['sender']
    content = data['content']
    course_name = data['course_name']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("INSERT INTO messages(sender, content, course_name) VALUES (%s, %s, %s)",
                   (sender, content, course_name))
    mysql.connection.commit()
    emit('new_message', {'sender': sender, 'content': content})

@app.route('/submit_feedback', methods=['GET', 'POST'])
def submit_feedback():
    if request.method == 'POST':
        course_id = request.form['course_id']
        rating = int(request.form['rating'])
        feedback_comments = request.form['feedback_comments']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO feedback (course_id, rating, feedback_comments) VALUES (%s, %s, %s)",(course_id, rating, feedback_comments))
        mysql.connection.commit()
        return redirect(url_for('submit_feedback'))

    return render_template('feedback_form.html')

@app.route('/courses/<int:course_id>')
def rating(course_id):
    # Query feedback data to calculate average rating for the course
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT AVG(rating) FROM feedback WHERE course_id = %s", (course_id,))
    average_rating = mycursor.fetchone()[0]

    return render_template('my_courses_mentee.html', average_rating=average_rating)
 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('hello'))

if __name__ == "__main__":
    with app.app_context():
        init_db()
    socketio.run(app)
            
 
