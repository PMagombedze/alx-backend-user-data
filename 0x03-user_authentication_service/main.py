#!/usr/bin/env python3


"""
integration test
"""


import requests

BASE_URL = 'http://localhost:5000'
EMAIL = "guillaume@holberton.io"
PASSWORD = "b4l0u"
NEW_PASSWORD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """
    validating user registration
    """
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(f'{BASE_URL}/users', data=data)

    message = {"email": email, "message": "user created"}

    assert response.status_code == 200
    assert response.json() == message


def log_in_wrong_password(email: str, password: str) -> None:
    """
    validating log in with incorrect password
    """
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(f'{BASE_URL}/sessions', data=data)

    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    validating succesful log in
    """
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(f'{BASE_URL}/sessions', data=data)

    message = {"email": email, "message": "logged in"}

    assert response.status_code == 200
    assert response.json() == message

    session_id = response.cookies.get("session_id")

    return session_id


def profile_unlogged() -> None:
    """
    validating profile request without login
    """
    cookies = {
        "session_id": ""
    }
    response = requests.get(f'{BASE_URL}/profile', cookies=cookies)

    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    validating profile
    """
    cookies = {
        "session_id": session_id
    }
    response = requests.get(f'{BASE_URL}/profile', cookies=cookies)

    message = {"email": EMAIL}

    assert response.status_code == 200
    assert response.json() == message


def log_out(session_id: str) -> None:
    """
    validating log out
    """
    cookies = {
        "session_id": session_id
    }
    response = requests.delete(f'{BASE_URL}/sessions', cookies=cookies)

    message = {"message": "Bienvenue"}

    assert response.status_code == 200
    assert response.json() == message


def reset_password_token(email: str) -> str:
    """
    validating password reset token
    """
    data = {
        "email": email
    }
    response = requests.post(f'{BASE_URL}/reset_password', data=data)

    assert response.status_code == 200
    resetToken = response.json().get("resetToken")
    message = {"email": email, "resetToken": resetToken}
    assert response.json() == message

    return resetToken


def update_password(email: str, resetToken: str, new_password: str) -> None:
    """
    validating password reset
    """
    data = {
        "email": email,
        "resetToken": resetToken,
        "new_password": new_password
    }
    response = requests.put(f'{BASE_URL}/reset_password', data=data)
    message = {"email": email, "message": "Password updated"}
    assert response.status_code == 200
    assert response.json() == message


if __name__ == "__main__":

    register_user(EMAIL, PASSWORD)
    log_in_wrong_password(EMAIL, NEW_PASSWORD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWORD)
    profile_logged(session_id)
    log_out(session_id)
    resetToken = reset_password_token(EMAIL)
    update_password(EMAIL, resetToken, NEW_PASSWORD)
    log_in(EMAIL, NEW_PASSWORD)
