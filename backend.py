""""""

import base64
import csv
import io
import json
import string
from datetime import datetime
from io import BytesIO

import IPython
from flask import (Flask, jsonify, redirect, render_template, request,
                   send_file, url_for)
from flask_login import LoginManager, UserMixin, login_required
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()

app = Flask(__name__)
app.config.from_object('config')
app.config.from_pyfile('config.py')
login_manager.init_app(app)

db = SQLAlchemy(app)

@app.route("/")
def hello():
    return "hello world"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
