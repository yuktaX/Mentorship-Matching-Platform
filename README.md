## To run the application

#### Create a virtual environment

#### Virtual environment creation:(windows)
virtualenv env

Virtual environment activation:
env\Scripts\activate.ps1

In the virtual environment run the following commands in terminal:
pip install flask
pip install flask_mysqldb

#### Running the application

Run the following command:
python app.py
The application will start running on localhost 

For now schema.sql needs to be run manually on mySQL workbench


#### All html files are inside templates folder and the asset folder has been migrated inside the static folder
All href links inside html files to the asset folder has been replaced by /..static/assets/ from assets/

All href links to .html files have been replaced to their URLs (in most cases removed the .html part ---> login.html replaced by /login). Appropriate functions for handling URLS have been added

Schema used is just a demo schema. Will update later
