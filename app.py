#!/usr/bin/python
from flask import Flask, render_template, request, redirect, session, flash, url_for
from functools import wraps
import teacher_dbhelper as teacherdb
import student_dbhelper as studentdb

app = Flask(__name__)
app.secret_key = open('session_key.txt', 'r').read().strip()

def redirect_if_logged_in(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if session.has_key('email') and session.has_key('userType'):
            if session['userType'] == 'teacher':
                return redirect(url_for('teacher'))
            elif session['userType'] == 'student':
                return redirect(url_for('student'))
            else:
                return redirect(url_for('index'))
        return func()
    return inner

@app.route('/')
@redirect_if_logged_in
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
@redirect_if_logged_in
def login():
    if request.method == 'POST':
        if request.form.has_key('email') and\
           request.form.has_key('password') and\
           request.form.has_key('userType'):
            email = request.form['email']
            pword = request.form['password']
            utype = request.form['userType']
            if utype == 'teacher':
                response_tuple = teacherdb.validate(email, pword)
                flash(response_tuple[1])
                if response_tuple[0]:
                    session['email'] = email
                    session['userType'] = 'teacher'
                    return redirect(url_for('teacher'))
                else:
                    return redirect(url_for('login'))
            elif utype == 'student':
                response_tuple = studentdb.validate(email, pword)
                flash(response_tuple[1])
                if response_tuple[0]:
                    session['email'] = email
                    session['userType'] = 'student'
                    return redirect(url_for('student'))
                else:
                    return redirect(url_for('login'))
            else: # userType field is invalid
                flash("Invalid request")
                return render_template('login.html')
        else: # Request is missing fields
            flash("Invalid request")
            return render_template('login.html')
    else: # Request is not POST
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
@redirect_if_logged_in
def register():
    if request.method == 'POST':
        if request.form.has_key('email') and\
           request.form.has_key('password') and\
           request.form.has_key('userType'):
            email = request.form['email']
            pword = request.form['password']
            utype = request.form['userType']
            if utype == 'teacher':
                response_tuple = teacherdb.insert(email, pword)
                flash(response_tuple[1])
                if response_tuple[0]:
                    return redirect(url_for('login'))
                else:
                    return render_template('register.html')
            elif utype == 'student':
                response_tuple = studentdb.insert(email, pword)
                flash(response_tuple[1])
                if response_tuple[0]:
                    return redirect(url_for('login'))
                else:
                    return render_template('register.html')
            else: # userType field is invalid
                flash("Invalid request")
                return render_template('register.html')
        else: # Request is missing fields
            flash("Invalid request")
            return render_template('register.html')
    else: # Request is not POST
        return render_template('register.html')

@app.route('/logout')
def logout():
    if session.has_key('email'):
        session.clear()
        flash("Sucessfully logged out.")
    return redirect(url_for('index'))

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/teacher')
def teacher():
    if session.has_key('email') and\
       session.has_key('userType') and\
       session['userType'] == 'teacher':
        teacher = teacherdb.get(session['email'])
        if teacher.count() == 1:
            return render_template('teacher.html', teacher_id=teacher[0]['_id'])
    # Clear session dictionary to remove invalid data
    session.clear()
    return redirect(url_for('index'))

@app.route('/teacher/profile/<teacher_id>')
def teacher_profile(teacher_id=None):
    return render_template('teacher.html', teacher_id=teacher_id)

@app.route('/teacher/settings', methods=['GET', 'POST'])
def teacher_settings():
    if session.has_key('email') and\
       session.has_key('userType') and\
       session['userType'] == 'teacher':
        if request.method == 'POST':
            if request.form.has_key('name') and\
               request.form.has_key('school') and\
               request.form.has_key('email') and\
               request.form.has_key('new_password') and\
               request.form.has_key('password'):
                response_tuple = teacherdb.validate(session['email'],
                                      request.form['password'])
                if response_tuple[0]:
                    response_tuple = teacherdb.update(session['email'],
                            new_email=request.form['email'],
                            name=request.form['name'], school=request.form['school'],
                            password=request.form['new_password'])
                    flash(response_tuple[1])
                else:
                    flash(response_tuple[1])
            else:
                flash("Invalid request")
                return redirect(url_for('teacher'))
        teacher = teacherdb.get(session['email'])
        if teacher.count() == 1:
            teacher_data = teacher[0]
            return render_template('teacher_settings.html',
                    teacher_data=teacher_data)
    # Clear session dictionary to remove invalid data
    session.clear()
    return redirect(url_for('index'))

@app.route('/student')
def student():
    if session.has_key('email') and\
       session.has_key('userType') and\
       session['userType'] == 'student':
        student = studentdb.get(session['email'])
        if student.count() == 1:
            return render_template('student.html', student_id=student[0]['_id'])
    # Clear session dictionary to remove invalid data
    session.clear()
    return redirect(url_for('index'))

@app.route('/student/profile/<student_id>')
def student_profile(student_id=None):
    return render_template('student.html', student_id=student_id)

@app.route('/student/settings', methods=['GET', 'POST'])
def student_settings(student_id=None):
    if session.has_key('email') and\
       session.has_key('userType') and\
       session['userType'] == 'student':
        if request.method == 'POST':
            if request.form.has_key('name') and\
               request.form.has_key('email') and\
               request.form.has_key('new_password') and\
               request.form.has_key('password'):
                response_tuple = studentdb.validate(session['email'],
                                      request.form['password'])
                if response_tuple[0]:
                    response_tuple = studentdb.update(session['email'],
                            new_email=request.form['email'],
                            name=request.form['name'],
                            password=request.form['new_password'])
                    flash(response_tuple[1])
                else:
                    flash(response_tuple[1])
            else:
                flash("Invalid request")
                return redirect(url_for('student'))
        student = studentdb.get(session['email'])
        if student.count() == 1:
            student_data = student[0]
            return render_template('student_settings.html',
                    student_data=student_data)
    # Clear session dictionary to remove invalid data
    session.clear()
    return redirect(url_for('index'))

@app.route('/messages')
def messages():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return "Sorry, nothing at this URL.", 404

#======================END-DEFINITIONS======================

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0')
