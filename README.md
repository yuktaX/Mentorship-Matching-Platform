# To run the application

### Create a virtual environment

#### Virtual environment creation:(windows)
virtualenv env

Virtual environment activation:
env\Scripts\activate.ps1

In the virtual environment run the following commands in terminal:
pip install flask,flask_mysqldb

#### Create a folder static and insert the assets folder into it

## Running the application

Run the following command:
python app.py
The application will start running on localhost 


#### All html files are inside templates folder and the asset folder has been migrated inside the static folder
All href links inside html files to the asset folder has been replaced by ../static/assets/ from assets/

All href links to .html files have been replaced to their URLs (in most cases removed the .html part ---> login.html replaced by /login). Appropriate functions for handling URLS have been added

#### Schema.sql file is run at the start of program by init_db() function. No manual initialization required anymore. All table creations are hence present in schema.sql file.

### Added smtplib for emailing. Server sends a mail to mentees and mentors that they have completed signup and can login. Mentors are also asked to upload resume for approval.

#### How to execute?
Replace "mentify@example.com" with your email_id. Email will be sent from your email id. In place of passcode add google app password. Type in app password in google. Enable 2 factor authentication if not enabled. Create a app name. An app password will be generated. Copy it and replace passcode with it. Now you can send mails to mentor/mentee email_id from your email_id.

Payment.html and stylesheet created but not linked with backend yet.

#### For file uploads, create a folder for example 'file_uploads'.
Add path of the file_uploads in app.config like this : app.config['UPLOAD_FOLDER']='C:\\..\\mentorship_matching_platform\\file_uploads'

#### Change in schema
In mentor table, an attribute file_name added which stores name of resume file
In mentee attributes education and interests added
Course table modified adding a few attributes
Added tag relation tables in the schema

#### Forgot password functionality implemented.
Sends OTP in your mail. Password updated only on entering correct mail. On password update, an intimation is sent on mail

#### Profile viewing and updating successfully implemented for mentee
In profile updating you can also select tags which interest you
