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
    register = request.form['register']
    submit = request.form['submit']
    email = request.form['mail']
    pword = request.form['password']
    
    if register and submit and email and pword:
        # TODO
        pass
    return render_template("login.html")

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
