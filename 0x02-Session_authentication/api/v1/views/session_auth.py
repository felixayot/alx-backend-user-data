#!/usr/bin/env python3
"""Views for Session Authentication."""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """POST /api/v1/auth_session/login
    Return:
      - User object JSON represented
      - 400 if email or password is missing
      - 404 if user is not found
      - 401 if email or password is invalid
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if user is None or len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    SESSION_ID = getenv('SESSION_NAME')
    response.set_cookie(SESSION_ID, session_id)
    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def session_logout() -> str:
    """DELETE /api/v1/auth_session/logout
    Return:
      - empty JSON
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({})
    abort(404)
