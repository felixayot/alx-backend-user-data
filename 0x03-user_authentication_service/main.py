#!/usr/bin/env python3
"""Main file for integration testing of
   the authentication service.
"""
import requests


def register_user(email: str, password: str) -> None:
    """Test the register_user method."""
    data = {"email": email, "password": password}
    response = requests.post(
        "http://localhost:5000/users",
        data=data)
    msg = {'email': email, 'message': 'user created'}
    error_msg = {'message': 'email already registered'}
    try:
        assert response.status_code == 200
        assert response.json() == msg
    except ValueError:
        assert response.status_code == 400
        assert response.json() == error_msg


def log_in_wrong_password(email: str, password: str) -> None:
    """Test the valid_login method."""
    data = {"email": email, "password": password}
    response = requests.post(
        "http://localhost:5000/sessions",
        data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test the create_session method."""
    data = {"email": email, "password": password}
    response = requests.post(
        "http://localhost:5000/sessions",
        data=data)
    msg = {"email": email, "message": "logged in"}
    assert response.status_code == 200
    assert response.json() == msg
    return response.cookies["session_id"]


def profile_unlogged() -> None:
    """Test the get_user_from_session_id method."""
    response = requests.get("http://localhost:5000/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test the get_user_from_session_id method."""
    response = requests.get(
        "http://localhost:5000/profile",
        cookies={"session_id": session_id})
    try:
        assert response.status_code == 200
        assert response.json() == {
            "email": response.json()["email"]
            }
    except ValueError:
        assert response.status_code == 403


def log_out(session_id: str) -> None:
    """Test the destroy_session method."""
    response = requests.delete(
        "http://localhost:5000/sessions",
        cookies={"session_id": session_id})
    msg = {"message": "Bienvenue"}
    assert response.status_code == 200
    assert response.json() == msg


def reset_password_token(email: str) -> str:
    """Test the get_reset_password_token method."""
    data = {"email": email}
    response = requests.post(
        "http://localhost:5000/reset_password", data=data)
    msg = {
        "email": email,
        "reset_token": response.json()["reset_token"]
        }
    assert response.status_code == 200
    assert response.json() == msg
    return response.json()["reset_token"]


def update_password(email: str,
                    reset_token: str,
                    new_password: str) -> None:
    """Test the update_password method."""
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
        }
    response = requests.put(
        "http://localhost:5000/reset_password",
        data=data)
    msg = {"email": email, "message": "Password updated"}
    assert response.status_code == 200
    assert response.json() == msg


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
    print("***All tests passed***")
