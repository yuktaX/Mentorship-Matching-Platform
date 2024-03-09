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

## Schema.sql file is run at the start of program by init_db() function. No manual initialization required anymore. All table creations are hence present in schema.sql file.
