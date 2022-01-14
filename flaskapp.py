from logging import Manager
from flask import Flask, json,jsonify
from fii_api import main

app = Flask(__name__)

@app.route("/")
def json_api():
    jsoni = jsonify(dict(main()))
    return jsoni

app.run(debug=True)
