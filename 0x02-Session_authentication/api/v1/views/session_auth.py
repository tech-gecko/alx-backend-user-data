#!/usr/bin/env python3
""" Module of session auth views
"""
from api.v1.views import app_views
from flask import jsonify, request
from ....models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth():
    """
        GET api/v1/auth_session/login
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

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({'error': 'wrong password'}), 401

    response = jsonify(user.to_json())

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response.set_cookie(session_id, user.id)

    return response, 201
