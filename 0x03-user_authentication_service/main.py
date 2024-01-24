#!/usr/bin/env python3
"""
Main file for testing web server for the corresponding end-points.
"""
import requests


def register_user(email: str, password: str) -> None:
    """
    Test for register a user with the given email and password.
    Args:
        email: The email of the user.
        password: The password of the user.
    Returns:
        None
    """
    base_url = 'http://127.0.0.1:5000'
    data = {'email': email, 'password': password}
    r = requests.post(base_url + '/users', data)
    if r.status_code == 200:
        assert r.json() == {"email": email, "message": "user created"}
    else:
        assert r.status_code == 400
        assert r.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Test for log in with the given wrong credentials.
    Args:
        email: The email of the user.
        password: The password of the user.
    Returns:
        None
    """
    base_url = 'http://127.0.0.1:5000'
    data = {'email': email, 'password': password}
    response = requests.post(base_url + '/sessions', data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Test for log in with the given correct email and password.
    Args:
        email: The email of the user.
        password: The password of the user.
    Returns:
        The session_id of the user.
    """
    base_url = 'http://127.0.0.1:5000'
    data = {'email': email, 'password': password}
    response = requests.post(base_url + '/sessions', data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """
    Test for profile without being logged in with session_id.
    Returns:
        None
    """
    base_url = 'http://127.0.0.1:5000'
    r = requests.get(base_url + '/profile')
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Test for profile with being logged in with session_id.
    Args:
        session_id: The session_id of the user.
    Returns:
        None
    """
    base_url = 'http://127.0.0.1:5000'
    cookie = {'session_id': session_id}
    response = requests.get(base_url + '/profile', cookies=cookie)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """
    Test for log out with the given session_id.
    Args:
        session_id: The session_id of the user.
    Returns:
        None
    """
    base_url = 'http://127.0.0.1:5000'
    cookies = {'session_id': session_id}
    response = requests.delete(base_url + '/sessions', cookies=cookies)
    if response.status_code == 302:
        assert response.url == 'http://127.0.0.1:5000'
    else:
        assert response.status_code == 403


def reset_password_token(email: str) -> str:
    """
    Test for reset password token with the given email.
    Args:
        email: The email of the user.
    Returns:
        The reset_token of the user.
    """
    base_url = 'http://127.0.0.1:5000'
    data = {'email': email}
    response = requests.post(base_url + '/reset_password', data=data)
    if response.status_code == 200:
        return response.json().get('reset_token')
    else:
        assert response.status_code == 403


def update_password(email: str, reset_token: str,
                    new_password: str) -> None:
    """
    Test for update password with the given email,
    reset_token and new_password.
    Args:
        email: The email of the user.
        reset_token: The reset_token of the user.
        new_password: The new password of the user.
    Returns:
        None
    """
    base_url = 'http://127.0.0.1:5000'
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    response = requests.put(base_url + '/reset_password', data=data)
    if response.status_code == 200:
        expected = {"email": email, "message": "Password updated"}
        assert response.json() == expected
    else:
        assert response.status_code == 403


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
