@app.route('/submit_mentee_complaint', methods=['POST'])
def submit_mentee_complaint():
    mentee_id = request.form['mentee_id']
    complaint_date = request.form['complaint_date']
    complaint_desc = request.form['complaint_desc']
    
    cursor = db.cursor()
    cursor.execute("INSERT INTO mentee_complaints (mentee_id, complaint_date, complaint_desc) VALUES (%s, %s, %s)", (mentee_id, complaint_date, complaint_desc))
    db.commit()
    cursor.close()
    
    return redirect(url_for('index'))

@app.route('/submit_mentor_complaint', methods=['POST'])
def submit_mentor_complaint():
    mentor_id = request.form['mentor_id']
    complaint_date = request.form['complaint_date']
    complaint_desc = request.form['complaint_desc']
    
    cursor = db.cursor()
    cursor.execute("INSERT INTO mentor_complaints (mentor_id, complaint_date, complaint_desc) VALUES (%s, %s, %s)", (mentor_id, complaint_date, complaint_desc))
    db.commit()
    cursor.close()
    
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM mentee_complaints WHERE complaint_status='pending'")
    mentee_pending_complaints = cursor.fetchall()
    cursor.execute("SELECT * FROM mentor_complaints WHERE complaint_status='pending'")
    mentor_pending_complaints = cursor.fetchall()
    cursor.close()
    
    return render_template('index', mentee_complaints=mentee_pending_complaints, mentor_complaints=mentor_pending_complaints)

@app.route('/resolve_mentee_complaint/<int:complaint_id>')
def resolve_mentee_complaint(complaint_id):
    cursor = db.cursor()
    cursor.execute("UPDATE mentee_complaints SET complaint_status='resolved', complaint_action='Resolved' WHERE complaint_id=%s", (complaint_id,))
    db.commit()
    cursor.close()
    
    return redirect(url_for('admin'))

@app.route('/resolve_mentor_complaint/<int:complaint_id>')
def resolve_mentor_complaint(complaint_id):
    cursor = db.cursor()
    cursor.execute("UPDATE mentor_complaints SET complaint_status='resolved', complaint_action='Resolved' WHERE complaint_id=%s", (complaint_id,))
    db.commit()
    cursor.close()
    
    return redirect(url_for('admin'))
