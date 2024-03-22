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
def view_course(course_id):
    # Query feedback data to calculate average rating for the course
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT AVG(rating) FROM feedback WHERE course_id = %s", (course_id,))
    average_rating = mycursor.fetchone()[0]

    return render_template('my_courses_mentee.html', average_rating=average_rating)
