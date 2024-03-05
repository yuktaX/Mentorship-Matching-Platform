from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
 
 
app = Flask(__name__)
#from app import routes, models
 
app.secret_key = 'your secret key'


 
 
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '281613'
app.config['MYSQL_DB'] = 'mentify'
 
 
mysql = MySQL(app)

@app.route('/')
def hello():
    return render_template('landing.html')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/process_login',methods=['GET','POST'])
def process_login():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username=request.form['username']
        password=request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM mentee WHERE username = % s \
            AND pass_word = % s', (username, password,) )
        account=cursor.fetchone()
        if account:
            session['loggedin']=True
            #session['name']=account['name']
            return render_template('index.html')
        else:
            cursor.execute(
            'SELECT * FROM mentor WHERE username = % s \
            AND pass_word = % s', (username, password,) )
            account=cursor.fetchone()
            if account:
                session['loggedin']=True
                #session['name']=account['name']
                return render_template('index.html')
            else:
                msg="Incorrect username/password!!"
                return render_template('landing.html',msg=msg)
    # return render_template('login.html')
        
#@app.route('\signup_process',methods=['GET','POST'])
#def signup_process():
 #   msg=''
  #  if request.method=='POST'and 'Full name' in request.form and 'Email address' in request.form and 'Phone number' in request.form  and 
@app.route('/signup_main')
def signup_main():
    return render_template('signup_main.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')



if __name__ == "__main__":
    app.run(debug=True)
            
 