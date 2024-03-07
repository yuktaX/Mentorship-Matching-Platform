
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import mysql.connector
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
#from app import routes, models

pin="@Tarushi15mad"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:password@localhost/mentify"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)


class mentee(db.Model):
    __tablename__="mentee"
    mentee_id = db.Column(db.Integer, primary_key=True,nullable=False,autoincrement=True)
    name = db.Column(db.String(100))
    contact_no = db.Column(db.String(10))
    email_id = db.Column(db.String(100))
    password = db.Column(db.String(15), nullable=False, unique=True)
    category = db.relationship('mentee_category', backref='mentee')
    username=db.Column(db.String(100),unique=True)

    def __init__(self, name,contact_no, email_id,password):
        self.name = name
        self.contact_no = contact_no
        self.email_id = email_id
        self.password=password

def create_db():
    with app.app_context():
        db.create_all()
  
class mentor(db.Model):
    __tablename__="mentor"
    mentor_id = db.Column(db.Integer, primary_key=True,nullable=False,autoincrement=True)
    name = db.Column(db.String(100))
    contact_no = db.Column(db.String(10))
    email_id = db.Column(db.String(100))
    qualification = db.Column(db.String(100))
    work_exp = db.Column(db.String(255))
    password = db.Column(db.String(15), nullable=False, unique=True)
    username=db.Column(db.String(100),unique=True)

class category(db.Model):
    __tablename__="category"
    category_id = db.Column(db.Integer, primary_key=True,nullable=False,autoincrement=True)
    category_name = db.Column(db.String(100))
    int_category = db.relationship('mentee_category', backref='category')

class mentee_category(db.Model):
    __tablename__="mentee_category"
    category_id = db.Column(db.Integer,db.ForeignKey('category.category_id'),primary_key=True)
    mentee_id = db.Column(db.Integer,db.ForeignKey('mentee.mentee_id'),primary_key=True) 

class mentorship_prog(db.Model): 
    program_id = db.Column(db.Integer, primary_key=True,nullable=False,autoincrement=True)
    mentee_id = db.Column(db.Integer,db.ForeignKey('mentee.mentee_id'))
    mentor_id = db.Column(db.Integer,db.ForeignKey('mentor.mentor_id'))
    category_id = db.Column(db.Integer,db.ForeignKey('category.category_id'))
    payment = db.Column(db.Integer)
    status=db.Column(db.String(10))



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
        user = mentee.query.filter_by(username=request.form.get("username")).first()
        if user:
            if user.password == request.form.get("password"):
                session['loggedin']=True
                return redirect(url_for("dashboard"))
            msg="incorrect username or password"
            return render_template("login.html",msg=msg)
        else:
            user = mentor.query.filter_by(username=request.form.get("username")).first() 
            if user:
              if user.password == request.form.get("password"):
                session['loggedin']=True
                return redirect(url_for("dashboard"))
            msg="incorrect username or password"
            return render_template("login.html",msg=msg)
        

@app.route('/signup_main',methods=['GET','POST'])
def signup_main():
    if request.method=='POST':
        type=request.form['name']
        return render_template("signup.html")

@app.route('/signup',methods=['GET','POST'])
def signup_process():
    msg=''
    if request.method=='POST':
        if type=="mentee": 
            name = request.form['name']
            contact_no = request.form['contact_no']
            email_id = request.form['email']
            password = request.form['password']
            #username = request.form['username']
            new_user=mentee(name=name,contact_no=contact_no,email_id=email_id,password=password)#,username=username)
            db.session.mentee.add(new_user)
            db.session.commit()
        else:
            name = request.form['name']
            contact_no = request.form['contact_no']
            email_id = request.form['email']
            password = request.form['password']
            #username = request.form['username']
            #qualification=request.form['qualification']
           # work_exp=request.form['work_exp']
            new_user=mentor(name=name,contact_no=contact_no,email_id=email_id,password=password)#,username=username,qualification=qualification,work_exp=work_exp)
            db.session.mentor.add(new_user)
            db.session.commit()

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('landing'))

if __name__ == "__main__":
    with app.app_context():
        # Create database tables
        db.create_all()
    app.run(debug=True)

