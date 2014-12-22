#!/usr/bin/python
from flask import Flask, render_template, request, redirect, session, flash
from functools import wraps

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

app.secret_key = open('session_key.txt', 'r').read().strip()

if __name__ == "__main__":
    app.debug=True
    app.run(host="0.0.0.0")
