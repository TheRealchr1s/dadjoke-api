"""App for dadjokes."""
import json
import os
import random

from flask import Flask, jsonify

PORT = int(os.environ.get("PORT", 5000))
INFO_HTML = "<h1>Endpoints:<br><br>GET /api/v1/dadjoke<br>GET /api/v1/joke</h1>"

APP = Flask(__name__)

with open("jokes.json", "r") as f:
    CACHE = tuple(json.loads(f.read()).values())


@APP.route("/")
@APP.route("/api")
@APP.route("/info")
def info():
    """Shows info for the API"""
    return INFO_HTML


@APP.route("/api/v1/joke")
@APP.route("/api/v1/dadjoke")
def joke():
    """Gets a joke"""
    return jsonify(
        dict(joke=random.choice(CACHE), status=200)
    )


if __name__ == "__main__":
    APP.run(host="0.0.0.0", debug=True, port=PORT)
