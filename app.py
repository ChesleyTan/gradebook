#!/usr/bin/python
from flask import Flask, render_template, request, redirect, session, flash
from functools import wraps

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
        if escape(session['utype'])=='teacher':
        return render_template("teacher.html", email, pword)
    elif method='POST':
        email = request.form['email']
        pword = request.form['password']
        name = request.form['name']
        utype = request.form['usertype']
        if utype=='teacher':
            school = request.form['school']

    register = request.form['register']
    submit = request.form['submit']
    
    if register:
        if utype=='teacher':
            if insert(email, pword, name, ):
            flash("You have successfully register for an account")
        else:
            flash("Email or password are already in use")
        return render_template("login.html")
    elif submit:
        if validate(email, pword):
            return redirect(url_for(
            
        
        # TODO
        pass
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
