#!/usr/bin/env python3
""" Module of session authentication views
"""
from os import getenv
from typing import Tuple
from api.v1.views import app_views
from flask import abort, jsonify, request

from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def view_login() -> Tuple[str, int]:
    """ POST /api/v1/auth_session/login
    Return:
      - JSON representation of a User object.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or email.strip() == '':
        return jsonify({"error": "email missing"}), 400

    if not password or password.strip() == '':
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    wrong_password = True
    for i in range(len(users)):
        if users[i].is_valid_password(password):
            wrong_password = False
            break

    if wrong_password:
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(getattr(users[i], 'id'))
    response = jsonify(users[i].to_json())
    session_name = getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def view_logout() -> Tuple[str, int]:
    """ DELETE /api/v1/auth_session/logout
    Return:
      - an empty JSON dictionary with the status code 200
    """
    from api.v1.app import auth
    is_deleted = auth.destroy_session(request)
    if not is_deleted:
        abort(404)

    return jsonify({}), 200
