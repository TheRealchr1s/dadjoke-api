from flask import Flask, jsonify
import json
import random

app = Flask(__name__)

with open("jokes.json", "r") as f:
    cache = list(json.loads(f.read()).values())

@app.route("/")
@app.route("/api")
@app.route("/info")
def info():
    return "<h1>Endpoints:<br><br>GET /api/v1/dadjoke<br>GET /api/v1/joke</h1>"

@app.route("/api/v1/joke")
@app.route("/api/v1/dadjoke")
def joke():
    return jsonify(dict(joke=random.choice(cache), status=200))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)