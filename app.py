#!/usr/bin/python
from flask import Flask, render_template, request, redirect, session, flash
from functools import wraps
import teacher_dbhelper as teacherdb
import student_dbhelper as studentdb

app = Flask(__name__)
app.secret_key = open('session_key.txt', 'r').read().strip()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'email' in session:
        if session['userType'] == 'teacher':
            # TODO get user's email and pword
            return render_template("teacher.html", email, pword)
        elif session['userType'] == 'student':
            # TODO get user's email and pword
            return render_template("student.html", email, pword)
        else:
            # Error Handle
            pass
    elif request.method == 'POST':
        if request.form.has_key('email') and\
           request.form.has_key('password') and\
           request.form.has_key('name') and\
           request.form.has_key('userType') and\
           request.form.has_key('submit'):
            email = request.form['email']
            pword = request.form['password']
            name = request.form['name']
            utype = request.form['userType']
            buttonPressed = request.form['submit']
            if utype == 'teacher':
                if buttonPressed == 'register':
                    response_tuple = teacherdb.insert(email, pword, name)
                    flash(response_tuple[1])
                    return render_template("login.html")
                elif buttonPressed == 'submit':
                    response_tuple = teacherdb.validate(email, pword)
                    flash(response_tuple[1])
                    if response_tuple[0]:
                        return redirect(url_for('teacher'))
                    else:
                        return redirect(url_for('login'))
                else:
                    flash("Invalid request")
                    return render_template("login.html")
            elif utype == 'student':
                if buttonPressed == 'register':
                    response_tuple = studentdb.insert(email, pword, name)
                    flash(response_tuple[1])
                    return render_template("login.html")
                elif buttonPressed == 'submit':
                    response_tuple = studentdb.validate(email, pword)
                    flash(response_tuple[1])
                    if response_tuple[0]:
                        return redirect(url_for('student'))
                    else:
                        return redirect(url_for('login'))
            else: # userType field is invalid
                flash("Invalid request")
                return render_template("login.html")
        else: # Request is missing fields
            flash("Invalid request")
            return render_template("login.html")
    else: # Request is not POST
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('email',None)
    return redirect(url_for('index'))

@app.route("/user")
def user():
    return render_template("user.html")

@app.route("/teacher")
def teacher():
    return render_template("user.html")

@app.route("/student")
def student():
    return render_template("user.html")
#======================END-DEFINITIONS======================

if __name__ == "__main__":
    app.debug=True
    app.run(host="0.0.0.0")
