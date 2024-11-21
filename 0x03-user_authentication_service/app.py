#!/usr/bin/env python3
"""
    A simple Flask app with user authentication services.
"""
from auth import Auth
from flask import Flask, abort, jsonify, redirect, request, url_for

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """
        GET /
        Return:
         - The home page view.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """
        POST /users
        Registers a user if the user doesn't already exist in the DB.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
        Logs the user in if login info is correct.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    new_session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie('session_id', new_session_id)

    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> None:
    """
        Logs out the user (if exists) and deletes the session.
        It also redirects to home page on logout.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect(url_for('index'))


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """
        Gets the user profile
    """
    session_id = request.cookies.get('session_id')
    if not session_id or type(session_id) != str:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
