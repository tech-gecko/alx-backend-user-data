#!/usr/bin/env python3
""" Module of session auth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv
from typing import Tuple


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def create_session() -> Tuple[str, int]:
    """
        POST api/v1/auth_session/login
        Return:
            Session for authenticated user.
    """
    email = request.form.get('email')
    if not email:
        return jsonify({'error': 'email missing'}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({'error': 'password missing'}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({'error': "no user found for this email"}), 404
    if len(users) <= 0:
        return jsonify({'error': "no user found for this email"}), 404

    user = users[0]
    if user.is_valid_password(password):
        response = jsonify(user.to_json())

        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        cookie_name = getenv('SESSION_NAME')
        response.set_cookie(cookie_name, session_id)

        return response, 201

    return jsonify({'error': 'wrong password'}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def delete_session() -> Tuple[str, int]:
    """
        DELETE api/v1/auth_session/logout
        Logs out and deletes the session.
    """
    from api.v1.app import auth

    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
