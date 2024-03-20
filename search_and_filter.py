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
    return render_template('dashboard_mentee.html', data=data, tag=tag, selected_filter=selected_tag, sort_option=sort_choice, search_term=search_term, search_type=search_type)



if __name__ == '__main__':
  app.run(debug=True)

