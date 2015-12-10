from flask import Flask
from flask_s3 import FlaskS3

s3 = FlaskS3()

def start_app():
    app = Flask(__name__)
    app.config['FLASK_S3_BUCKET_NAME'] = 'emrec'

