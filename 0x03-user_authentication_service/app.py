#!/usr/bin/env python3
"""
    A simple Flask app with user authentication services.
"""
from flask import Flask, jsonify


app = Flask(__name__)

@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """
        GET /
        Return:
         - The home page view.
    """
    return jsonify({"message": "Bienvenue"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")