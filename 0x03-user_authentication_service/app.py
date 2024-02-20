#!/usr/bin/env python3
"""Basic flask app."""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome():
    """Index page."""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register():
    """Endpoint to regidter a user."""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """Endpoint to login a user."""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        if not session_id:
            abort(401)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """Endpoint to logout a user."""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('welcome'))
    else:
        abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    """Endpoint to get the user profile."""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """Endpoint to get the reset password token."""
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token})
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """Endpoint to update the password."""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
