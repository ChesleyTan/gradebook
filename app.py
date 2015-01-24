#!/usr/bin/python
from flask import Flask, render_template, request, redirect, session, flash, url_for
from functools import wraps
import teacher_dbhelper as teacherdb
import student_dbhelper as studentdb
import course_dbhelper as coursedb

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
        return func(*args, **kwargs)
    return inner

def redirect_if_not_logged_in(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if session.has_key('email') and session.has_key('userType'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return inner

def redirect_if_logged_in_and_not_teacher(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if session['userType'] == 'teacher':
            return func(*args, **kwargs)
        else:
            return redirect(url_for('index'))
    return inner

def redirect_if_logged_in_and_not_student(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if session['userType'] == 'student':
            return func()
        else:
            return redirect(url_for('index'))
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
@redirect_if_not_logged_in
def logout():
    session.clear()
    flash("Sucessfully logged out.")

@app.route('/teacher')
@redirect_if_not_logged_in
@redirect_if_logged_in_and_not_teacher
def teacher():
    teacher = teacherdb.get(session['email'])
    if teacher.count() == 1:
        return render_template('teacher.html', teacher_id=teacher[0]['_id'])

@app.route('/teacher/profile/<teacher_id>')
@redirect_if_not_logged_in
def teacher_profile(teacher_id=None):
    if teacher_id:
        teacher = teacherdb.get("", teacher_id)
        if teacher and teacher.count() == 1:
            return render_template('teacher_profile.html',
                                    teacher_data=teacher[0])
    return redirect(url_for('index'))

@app.route('/teacher/settings', methods=['GET', 'POST'])
@redirect_if_not_logged_in
@redirect_if_logged_in_and_not_teacher
def teacher_settings():
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
            return redirect(url_for('teacher_settings'))
        else:
            flash("Invalid request")
            return redirect(url_for('teacher'))
    else:
        teacher = teacherdb.get(session['email'])
        if teacher.count() == 1:
            teacher_data = teacher[0]
            return render_template('teacher_settings.html',
                    teacher_data=teacher_data)
        return redirect(url_for('index'))

@app.route('/teacher/courses', methods=['GET', 'POST'])
@redirect_if_not_logged_in
@redirect_if_logged_in_and_not_teacher
def teacher_courses():
    if request.method == 'POST':
        if request.form.has_key('name') and\
            request.form.has_key('description') and\
            request.form.has_key('delete_name') and\
            request.form.has_key('submit') and\
            request.form.has_key('password'):
            response_tuple = teacherdb.validate(session['email'],
                                request.form['password'])
            if response_tuple[0]:
                if request.form['submit'] == 'add':
                    teacher = teacherdb.get(session['email'])[0]
                    response_tuple = coursedb.insert(teacher['_id'],
                                        request.form['name'],
                                        request.form['description'])
                    if response_tuple[0]:
                        new_course_id = coursedb.getByTeacher(teacher['_id'],
                                        name=request.form['name'])[0]['_id']
                        teacherdb.addCourseId(session['email'], new_course_id)
                    flash(response_tuple[1])
                    return redirect(url_for('teacher_courses'))
                elif request.form['submit'] == 'delete':
                    teacher = teacherdb.get(session['email'])[0]
                    if coursedb.exists(teacher['_id'],
                            request.form['delete_name']):
                        course_id = coursedb.getByTeacher(teacher['_id'],
                                name=request.form['delete_name'])[0]['_id']
                        coursedb.remove(teacher['_id'],
                                        request.form['delete_name'])
                        teacherdb.removeCourseId(session['email'], course_id)
                        flash("Successfully removed course")
                    else:
                        flash("Error: Course not found")
                    return redirect(url_for('teacher_courses'))
                else:
                    flash("Invalid request")
                    return redirect(url_for('teacher_courses'))
            else:
                flash(response_tuple[1])
                return redirect(url_for('teacher_courses'))
        else:
            flash("Invalid request")
            return redirect(url_for('teacher_courses'))
    else:
        teacher = teacherdb.get(session['email'])
        if teacher.count() == 1:
            teacher_data = teacher[0]
            courses = []
            for courseId in teacher_data['courses']:
                course_cursor = coursedb.get(courseId)
                if course_cursor.count() == 1:
                    courses.append(course_cursor[0])
                else:
                    # Teacher's courses list has a stale entry, so delete it
                    teacherdb.removeCourseId(session['email'], courseId)
            return render_template('teacher_courses.html',
                                    teacher_data=teacher[0],
                                    courses=courses)
    return redirect(url_for('index'))

@app.route('/student')
@redirect_if_not_logged_in
@redirect_if_logged_in_and_not_student
def student():
    student = studentdb.get(session['email'])
    if student.count() == 1:
        return render_template('student.html', student_id=student[0]['_id'])
    return redirect(url_for('index'))

@app.route('/student/profile/<student_id>')
@redirect_if_not_logged_in
def student_profile(student_id=None):
    if student_id:
        student = studentdb.get("", student_id)
        if student.count() == 1:
            return render_template('student_profile.html',
                                    student_data=student[0])
    return redirect(url_for('index'))

@app.route('/student/settings', methods=['GET', 'POST'])
@redirect_if_not_logged_in
@redirect_if_logged_in_and_not_student
def student_settings(student_id=None):
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
            return redirect(url_for('student_settings'))
        else:
            flash("Invalid request")
            return redirect(url_for('student'))
    else:
        student = studentdb.get(session['email'])
        if student.count() == 1:
            student_data = student[0]
            return render_template('student_settings.html',
                    student_data=student_data)
    return redirect(url_for('index'))

@app.route('/messages')
@redirect_if_not_logged_in
def messages():
    return render_template('index.html')

@app.route('/course/<course_id>')
@redirect_if_not_logged_in
def course(course_id=None):
    if course_id:
        # Check that user has permission to view the course
        # Fetch the info for the course(name, description, assignments,
        # students, teacher)
        return render_template('course.html')
    else:
        return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return "Sorry, nothing at this URL.", 404

#======================END-DEFINITIONS======================

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0')
