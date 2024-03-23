# To run the application

### Create a virtual environment

#### Virtual environment creation:(windows)
virtualenv env

Virtual environment activation:
env\Scripts\activate.ps1

In the virtual environment run the following commands in terminal:
pip install -r requirements.txt

#### Create a folder static and insert the assets folder into it

## Running the application
Replace sender_email with your email address. Email will be sent from your email id. In place of passcode add google app password. Type in app password in google. Enable 2 factor authentication if not enabled. Create a app name. An app password will be generated. Copy it and replace passcode with it. Now you can send mails to mentor/mentee email_id from your email_id.

Run the following command:
python app.py
The application will start running on localhost

### Schema.sql file contains all tables of the database. No manual initialization is required


#### For file uploads, create a folder for example 'file_uploads'.
Add path of the file_uploads in app.config like this : app.config['UPLOAD_FOLDER']='C:\\..\\mentorship_matching_platform\\file_uploads'



