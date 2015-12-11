import os
from flask import Flask
import sample_upload
import auth
app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello world!'

@app.route('/auth')
def a():
    auth()
    return 'a'
