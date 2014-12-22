#!/usr/bin/python
from flask import Flask, render_template, request, redirect, session, flash
from functools import wraps

app = Flask(__name__)



# Tmp, make an actual one when we deploy
app.secret_key = '\x90\x9c\xe3C<\x12]^v0p\xde\xc7\xb2\xa1\xea\x90e\x10\xfe\xf1\xd0\xa7g'

if __name__ == "__main__":
    app.debug=True
    app.run(host="0.0.0.0")
