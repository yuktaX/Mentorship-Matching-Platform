from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection details
config = {
  'user': 'your_username',
  'password': 'your_password',
  'host': 'your_host',
  'database': 'your_database'
}

def connect_to_database():
  """Connects to the MySQL database."""
  try:
    return mysql.connector.connect(**config)
  except mysql.connector.Error as err:
    print(err)
    return None

@app.route('/')
def index():
  """Renders the main page with initial data."""
  connection = connect_to_database()
  if connection is None:
    return "Error connecting to database"

  cursor = connection.cursor()
  cursor.execute("SELECT * FROM your_table")  # Replace with your table name
  data = cursor.fetchall()
  connection.close()

  return render_template('index.html', data=data)

@app.route('/search', methods=['POST'])
def search():
   """Searches the database based on mentor or course name."""
    connection = connect_to_database()
    if connection is None:
        return "Error connecting to database"

    mentor_name = request.form['mentor_name']
    cursor = connection.cursor()
    # Join with mentor table to get mentor name
    cursor.execute("""
        SELECT course.*, mentor.mentor_name
        FROM course
        JOIN mentor ON course.mentor_id = mentor.mentor_id 
        WHERE mentor.mentor_name LIKE %s OR course.course_name LIKE %s
    """,("%" + search_term + "%", "%" + search_term + "%"))
    data = cursor.fetchall()
    connection.close()

    return render_template('index.html', data=data)

@app.route('/filter', methods=['POST'])
def filter():
    """Filters data based on selected tags."""
    connection = connect_to_database()
    if connection is None:
        return "Error connecting to database"

    selected_tags = request.form.getlist('tags')

    cursor = connection.cursor()

    # Build dynamic query with OR clause for filtering based on tags
    query = """
        SELECT * FROM course
        WHERE %s IN (tag1, tag2, tag3, tag4, tag5)
    """

    # Execute the query for each selected tag
    data = []
    for tag in selected_tags:
        cursor.execute(query, (tag,))
        data.extend(cursor.fetchall())

    connection.close()

    return render_template('index.html', data=data)


@app.route('/sort')
def sort():
    """Sorts data based on the number of registrations in descending order.(popularity)"""
    connection = connect_to_database()
    if connection is None:
        return "Error connecting to database"

    cursor = connection.cursor()
    # Sort by number of registrations in descending order
    cursor.execute("SELECT * FROM course ORDER BY no_of_registrations DESC")
    data = cursor.fetchall()
    connection.close()

    return render_template('index.html', data=data)

if __name__ == '__main__':
  app.run(debug=True)

