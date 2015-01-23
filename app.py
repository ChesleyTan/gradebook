#!/usr/bin/python
from flask import Flask, render_template, request, redirect, session, flash
from functools import wraps
import teacher_dbhelper as teacherdb
import student_dbhelper as studentdb

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=['GET', 'POST'])
def login():

    if 'email' in session and rmber:
        if escape(session['utype']) == 'teacher':
            return render_template("teacher.html", email, pword)
        elif escape(session['utype']) == 'student':
            return render_template("student.html", email, pword)
    elif request.method == 'POST':
        email = request.form['email']
        pword = request.form['password']
        name = request.form['name']
        utype = request.form['usertype']
        register = request.form['register']
        login = request.form['login']
        if utype == 'teacher':
            school = request.form['school']
            if register:
                response_tuple = teacherdb.insert(email, pword, name, school)
                flash(response_tuple[1])
                return render_template("login.html")
            elif submit:
                response_tuple = teacherdb.validate(email, pword)
                if response_tuple[0]:
                    return redirect(url_for('teacher'))
                else:
                    return redirect(url_for('login'))
        elif utype == 'student':
            if register:
                response_tuple = studentdb.insert(email, pword, name)
                flash(response_tuple[1])
                return render_template("login.html")
            elif submit:
                response_tuple = studentdb.validate(email, pword)
                if response_tuple[0]:
                    return redirect(url_for('student'))
                else:
                    return redirect(url_for('login'))
        else:
            flash("Invalid request")
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('email',None)
    return redirect(url_for('home'))

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

app.secret_key = open('session_key.txt', 'r').read().strip()

if __name__ == "__main__":
    app.debug=True
    app.run(host="0.0.0.0")
