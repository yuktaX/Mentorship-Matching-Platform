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

@app.route('/search_sort_filter', methods=['POST'])
def search_sort_filter():
    """Sorts, searches, and filters data based on the provided parameters."""
    connection = connect_to_database()
    if connection is None:
        return "Error connecting to database"

    cursor = connection.cursor()

    # Default sorting option
    sort_option = "no_of_registrations DESC"

    # Default query without sorting, searching, or filtering
    query = """
        SELECT course.*, mentor.mentor_name
        FROM course
        JOIN mentor ON course.mentor_id = mentor.mentor_id
    """

    # Check if a sorting option is provided
    if 'sort' in request.form:
        sort_choice = request.form['sort']
        if sort_choice == 'valuation':
            sort_option = "no_of_registrations DESC"
        elif sort_choice == 'equity':
            sort_option = "course_price ASC"
        elif sort_choice == 'investment':
            sort_option = "course_price DESC"

    # Check if a tag is selected for filtering
    if 'filter' in request.form:
        selected_tag = request.form['filter']
        if selected_tag != 'none':
            # Apply filtering based on the selected tag
            query += """
                WHERE course.course_id IN (
                    SELECT course_id
                    FROM course_tag_relation
                    WHERE tag_id = (
                        SELECT tag_id
                        FROM tag
                        WHERE tag_name = %s
                    )
                )
            """

    # Apply sorting to the query
    query += f" ORDER BY {sort_option}"

    # Execute the final query with all applied parameters
    if 'search_term' in request.form:
        search_term = request.form['search_term']
        search_type = request.form['search_type']

        if search_term:
            if 'filter' not in request.form or selected_tag == 'none':
                # If no filtering is applied or filter is set to none, search without filtering
                query += """
                    WHERE
                """
            else:
                # If filtering is applied, append AND to the query
                query += """
                    AND
                """

            if search_type == 'mentor':
                query += """
                    mentor.mentor_name LIKE %s
                """
            elif search_type == 'course':
                query += """
                    course.course_name LIKE %s
                """

            # Execute the query with search parameters
            cursor.execute(query, ("%" + search_term + "%",))
        else:
            # Execute the query without search parameters
            cursor.execute(query)
    else:
        # Execute the query without search parameters
        cursor.execute(query)

    data = cursor.fetchall()
    connection.close()

    return render_template('index.html', data=data)




if __name__ == '__main__':
  app.run(debug=True)

