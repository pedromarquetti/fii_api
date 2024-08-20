from flask import Flask, json, jsonify, redirect
from src.helpers import get_data, open_and_read, write_to_file
app = Flask(__name__)

API_STR = "/api"

endpoints = {
    "update local json file": f"{API_STR}/update_json",
    "fii minimal": f"{API_STR}/fii/<string:name>"

}


@app.route(f"{endpoints['update local json file']}")
def update_json():
    try:
        data = get_data(True)
        write_to_file(data)
    except Exception as e:
        app.logger.error(e)
    return data


@app.errorhandler(404)
def not_found(_):
    return jsonify({
        "invalid endpoint! use this map": endpoints,
        "error": "404 - Not found"
    })


@app.route("/")
def root_response():
    return jsonify({"invalid endpoint! use this map": endpoints})


@app.route(f"{endpoints['fii minimal']}")
def get_fii(name: str):
    if not name.endswith("11"):
        return redirect("/404")
    else:
        data = open_and_read()
        return jsonify(data["BCFF11"])


app.run(debug=True)
