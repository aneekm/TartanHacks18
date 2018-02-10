""""""
import json

import IPython
from flask import (Flask, jsonify, redirect, render_template, request,
                   send_file, url_for)

app = Flask(__name__)
app.config.from_object('config')
app.config.from_pyfile('config.py')

@app.route("/")
def mainpage():
    params = ""
    return render_template("templates/index.html", params=params)

@app.route("/search/<search_term>")
def search(search_term):
    params = ""
    return render_template("templates/search.html", params=params)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
