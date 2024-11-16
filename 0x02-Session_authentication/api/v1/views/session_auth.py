#!/usr/bin/env python3
""" Module of session auth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def create_session() -> str:
    """
        POST api/v1/auth_session/login
        Return:
            Session for authenticated user.
    """
    not_found_resp = {"error": "no user found for this email"}

    email = request.form.get('email')
    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify(not_found_resp), 404
    if len(users) <= 0:
        return jsonify(not_found_resp), 404

    if users[0].is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(getattr(users[0], 'id'))
        resp = jsonify(users[0].to_json())
        resp.set_cookie(os.getenv("SESSION_NAME"), session_id)

        return resp

    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def delete_session() -> str:
    """
        DELETE api/v1/auth_session/logout
        Logs out and deletes the session.
    """
    from api.v1.app import auth

    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
