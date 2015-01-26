#!/usr/bin/python
from flask import Flask, render_template, request, redirect, session, flash, url_for
from functools import wraps
import teacher_dbhelper as teacherdb
import student_dbhelper as studentdb
import course_dbhelper as coursedb
import assignment_dbhelper as assignmentdb

import time
from datetime import date

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
                session.clear()
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
    # TODO Add name to register
    if request.method == 'POST':
        if request.form.has_key('name') and\
           request.form.has_key('email') and\
           request.form.has_key('password') and\
           request.form.has_key('userType'):
            name = request.form['name']
            email = request.form['email']
            pword = request.form['password']
            utype = request.form['userType']
            if utype == 'teacher':
                response_tuple = teacherdb.insert(name, email, pword)
                flash(response_tuple[1])
                if response_tuple[0]:
                    return redirect(url_for('login'))
                else:
                    return render_template('register.html')
            elif utype == 'student':
                response_tuple = studentdb.insert(name, email, pword)
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
    return redirect(url_for('index'))

@app.route('/teacher')
@redirect_if_not_logged_in
@redirect_if_logged_in_and_not_teacher
def teacher():
    teacher = teacherdb.get(session['email'])
    if teacher.count() == 1:
        return render_template('teacher.html', teacher_id=teacher[0]['_id'])
    else:
        session.clear()
        return redirect(url_for('index'))

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
                        new_course_id = str(coursedb.getByTeacher(teacher['_id'],
                                        name=request.form['name'])[0]['_id'])
                        response_tuple = teacherdb.addCourseId(session['email'], new_course_id)
                    flash(response_tuple[1])
                    return redirect(url_for('teacher_courses'))
                elif request.form['submit'] == 'delete':
                    teacher = teacherdb.get(session['email'])[0]
                    if coursedb.exists(teacher['_id'],
                            request.form['delete_name']):
                        course_id = str(coursedb.getByTeacher(teacher['_id'],
                                name=request.form['delete_name'])[0]['_id'])
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

#need to replace teacher['_id'] with courseID and adjust databse
#@app.route('/teacher/assignments', methods=['GET','POST'])
#def teacher_assignments():
#    if session.has_key('email') and\
#       session.hass_key('userType') and\
#       session['userType'] == 'teacher':
#        if request.method == 'POST':
#            if request.form.has_key('name') and\
#               request.form.has_key('description') and\
#               request.form.has_key('date') and\
#               request.form.has_key('delete_name') and\
#               request.form.has_key('submit') and\
#               requst.form.has_key('password'):
#                response_tuple = teacherdb.validate(session['email'],
#                                                    request.form['password'])
#                if response_tuple[0]:
#                    if request.form['submit'] == 'add':
#                        teacher = teacherdb.get(session['email'])[0]
#                        response_tuple = assignmentdb.insert(teacher['_id'],
#                                                             request.form['name'],
#                                                             request.form['description']
#                                                             request.form['date'])
#                        if response_tuple[0]:
#                            new_assignment_id = assignmentdb.getByTeacher(teacher'_id'],
#                            name=request.form['name')[0]['_id']
#                        flash(response_tuple[1])
#                        return redirect(url_for('teacher_assignments'))
#                    elif request.form['submit'] == 'delete':
#                        teacher = teacherdb.get(session['email'])[0]
#                        if assignmentdb.exists(teacher['_id'],
#                                               request.form['delete_name']):
#                            assignment_id = assignmentdb.get(teacher['_id'],
#                                                             request.form['delete_name'])
#                            assignmentdb.remove(teacher['_id'],
#                                              request.form['delete_name']
#                                              request.form['descript']
#                                              reqeust.form['date'])
#                            teacherdb.removeAssignmentID(seesion['email'], assignment_id)
#                            flash("Successfully removed assignment")
#                        else:
#                            flash("Error: Assignment not found")
#                        return redirect(url_for('teacher_assignments'))
#                    else:
#                        flash("Invalid request")
#                        return redirect(url_for('teacher_assignments'))
#                else:
#                    flash(response_tuple[1])
#                    return redirect(url_for('teacher_assignments'))
#            else:
#                flash("Invalid request")
#                return redirect(url_for('teacher_assignments'))
#        else:
#            teacher = teacherdb.get(session['email'])
#            if teacher.count() == 1:
#                teacher_data = teacher[0]
#                assignment = []
#                for assignmentId in teacher_data['assignment']:
#                    assignment_cursor = assignmentdb.get(assignmentId)
#                    if assignment_cursor.count() == 1:
#                        assignments.append(assignment_cursor[0])
#                    else:
#                        # Teacher's courses list has a stale entry, so delete it
#                        teacherdb.removeAssignmentId(session['email'], assignmentId)
#                return render_template('teacher_assignment.html',
#                                       teacher_data=teacher[0],
#                                       assignment=assignment)
#    return redirect(url_for('index'))

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

@app.route('/student/courses', methods=['GET', 'POST'])
@redirect_if_not_logged_in
@redirect_if_logged_in_and_not_student
def student_courses():
    if request.method == 'POST':
        if request.form.has_key('delete_name') and\
            request.form.has_key('password'):
            response_tuple = studentdb.validate(session['email'],
                                request.form['password'])
            if response_tuple[0]:
                student = studentdb.get(session['email'])[0]
                foundCourse = False
                for courseId in student['courses']:
                    course_cursor = coursedb.get(courseId)
                    if course_cursor and course_cursor.count() == 1:
                        course_cursor = course_cursor[0]
                        if course_cursor['name'] ==\
                           request.form['delete_name']:
                            foundCourse = True
                            course_id = str(coursedb.getByTeacher(
                                    course_cursor['teacherId'],
                                    name=request.form['delete_name'])[0]['_id'])
                            coursedb.remove(course_cursor['teacherId'],
                                    request.form['delete_name'])
                            studentdb.removeCourse(session['email'], course_id)
                            flash("Successfully left course")
                        if not foundCourse:
                            flash("Invalid course name")
                return redirect(url_for('student_courses'))
            else:
                flash(response_tuple[1])
                return redirect(url_for('student_courses'))
        else:
            flash("Invalid request")
            return redirect(url_for('student_courses'))
    else:
        student = studentdb.get(session['email'])
        if student.count() == 1:
            student_data = student[0]
            courses = []
            for courseId in student_data['courses']:
                course_cursor = coursedb.get(courseId)
                if course_cursor.count() == 1:
                    courses.append(course_cursor[0])
                else:
                    # Student's courses list has a stale entry, so delete it
                    studentdb.removeCourse(session['email'], courseId)
            return render_template('student_courses.html',
                                    student_data=student[0],
                                    courses=courses)
        return redirect(url_for('index'))

@app.route('/course/<course_id>', methods=['GET', 'POST'])
@redirect_if_not_logged_in
def course(course_id=None):
    if course_id:
        if request.method == 'GET':
            # Check that user has permission to view specific information
            hasPermissionToView = False
            if session['userType'] == 'student':
                hasPermissionToView = studentdb.hasCourse(session['email'],
                                                        course_id)
            elif session['userType'] == 'teacher':
                hasPermissionToView = teacherdb.hasCourse(session['email'],
                                                        course_id)
            course = coursedb.get(course_id)
            if course and course.count() == 1:
                course = course[0]
                teacher = teacherdb.get('', teacher_id=course['teacherId'])
                if teacher and teacher.count() == 1:
                    teacher = teacher[0]['name']
                    students = []
                    assignments = assignmentdbb.getByCourse(course_id)
                    if hasPermissionToView:
                        for studentId in course['students']:
                            student = studentdb.get('', student_id=studentId)
                            if student and student.count() == 1:
                                students.append(student[0])
                    if session['userType'] == 'student':
                        # showRequestButton flag:
                        # 0 -> Do not show
                        # 1 -> Show
                        # 2 -> Show disabled and pending
                        showRequestButton = 0
                        userId = studentdb.getId(session['email'])
                        if not studentdb.hasCourse(session['email'], course_id):
                            course_requests = coursedb.getCourseRequests(course_id)
                            if course_requests != None:
                                if userId not in course_requests:
                                    showRequestButton = 1
                                else:
                                    showRequestButton = 2
                        return render_template('course.html', course_data=course,
                                teacher=teacher, students=students,
                                showRequestButton=showRequestButton,
                                hasPermissionToView=hasPermissionToView,
                                assignments=assignments, userType=session['userType'])
                    else:
                        course_requests = coursedb.getCourseRequests(course_id)
                        requesters = []
                        for studentId in course_requests:
                            student = studentdb.get('', student_id=studentId)
                            if student and student.count() == 1:
                                requesters.append(student[0])
                        return render_template('course.html', course_data=course,
                                teacher=teacher, students=students,
                                hasPermissionToView=hasPermissionToView,
                                requesters=requesters,
                                assignments=assignments, userType=session['userType'])
        else:
            if session['userType'] == 'student':
                userId = studentdb.getId(session['email'])
                if userId:
                    coursedb.addCourseRequest(course_id, userId)
                    return redirect(url_for('course', course_id=course_id))
            else:
                if request.form.has_key('requester_id') and\
                   request.form.has_key('request_action'):
                    if request.form['request_action'] == 'accept':
                        if studentdb.exists('', request.form['requester_id']):
                            coursedb.addStudentToCourseAndRemoveRequest(course_id,
                                    request.form['requester_id'])
                            studentdb.addCourse(request.form['requester_id'],
                                                course_id)
                    else:
                        coursedb.removeCourseRequest(course_id,
                                request.form['requester_id'])

                if request.form.has_key('name') and\
                        request.form.has_key('description') and\
                        request.form.has_key('month') and\
                        request.form.has_key('day') and\
                        request.form.has_key('year') and\
                        request.form.has_key('aType') and\
                        request.form.has_key('delete_name') and\
                        request.form.has_key('password') and\
                        request.form.has_key('submit'):
                    response_tuple = teacherdb.validate(session['email'],
                                                        request.form['password'])
                    if response_tuple[0]:
                        if request.form['submit'] == 'add':
                            date = datetime.date(request.form['year'], request.form['month'], request.form['day'])
                            response_tuple = assignmentdb.insert(course_id, 
                                                                 request.form['name'], 
                                                                 request.form['description'], 
                                                                 date, 
                                                                 request.form['aType'])
                            flash(response_tuple[1])
                            return redirect(url_for('course', course_id=course_id))
                        elif request.form['submit'] == 'delete':
                            if assignmentdb.exists(course_id, 
                                                   request.form['delete_name']):
                                assignmentdb.remove(course_id,
                                                    request.form['delete_name'])
                                flash("Successfully removed assignment")
                            else:
                                flash("Error: Assignment not found")
                            return redirect(url_for('course', course_id=course_id))
                        else:
                            flash("Invalid request")
                            return redirect(url_for('course', course_id=course_id))
                    else:
                        flash(response_tuple[1])
                        return redirect(url_for('course', course_id=course_id))
                else:
                    flash("Invalid request")
                    return redirect(url_for('course', course_id=course_id))                             
                           

    return redirect(url_for('index'))

@app.route('/assignment/<course_id>/<name>', methods=['GET','POST'])
@redirect_if_not_logged_in
def assignment(course_id=None, name=None):
    if course_id and name:
        if request.method == 'GET':
            hasPermissionToView = False
            if session['userType'] == 'student':
                hasPermissionToView = studentdb.hasCourse(session['email'],
                                                          course_id)
            elif session['userType'] == 'teacher':
                hasPermissionToView = teacherdb.hasCourse(session['email'],
                                                          course_id)
            course = coursedb.get(course_id)
            if course and course.count() == 1:
                course = course[0]
                teacher = teacherdb.get('', teacher_id=course['teacherId'])
                if teacher and teacher.count() == 1:
                    teacher = teacher[0]['name']
                    students = []
                    assignment = assignmentdb.getByCourse(course_id)
                    if hasPermissionToView:
                        for studentId in course['students']:
                            student = studentdb.get('', student_id=studentId)
                            if student and student.count() == 1:
                                students.append(student[0])
            return render_template('assignment.html', course_data=course, 
                                   teacher=teacher, students=students, 
                                   hasPermissionToView=hasPermissionToView, 
                                   name=name, userType=session['userType'], 
                                   assignment=assignment)
        else:
            if session['userType'] == 'student':
                #something to do?
                return redirect(url_for('assignment', course_id=course_id, name=name))
            else:
                #TODO FINISH
                return redirect(url_for('assignment', course_id=course_id, name=name))
    else:
        return redirect(url_for('assignment', course_id=course_id, name=name))
    
@app.route('/messages')
@redirect_if_not_logged_in
def messages():
    if session['userType'] == 'student':
        student = studentdb.get(session['email'])
        if student.count() == 1:
            return render_template('messages.html', isStudent=True,
                        student_data=student[0])
    else:
        teacher = teacherdb.get(session['email'])
        if teacher.count() == 1:
            return render_template('messages.html', isTeacher=True,
                        teacher_data=teacher[0])

    # Page description:
    # Should list every other user that the current user 
    # has permission to contact. The list is sorted by
    # most recent message sent/recieved. 
    # Clicking takes you to that particular message page, /messages/<user>

@app.errorhandler(404)
def page_not_found(e):
    return "Sorry, nothing at this URL.", 404

#======================END-DEFINITIONS======================

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0')
