#!/usr/bin/env python3
from flask import Flask, jsonify


app = Flask(__name__)

@app.route('/', methods=['GET'], strict_slashes=False)
def hello():
    return jsonify({"message": "Bienvenue"})
