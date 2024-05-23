#!/usr/bin/env python3
""" view for users
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def user_login():
    """ helps the user to log in to there
        accounts
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    user_pwd = request.form.get('password')
    if not user_pwd:
        return jsonify({"error": "password missing"}), 400
    try:
        found_users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not found_users:
        return jsonify({"error": "no user found for this email"}), 404
    c_user = None
    for user in found_users:
        if user.is_valid_password(user_pwd):
            c_user = user
            break

    if not c_user:
        return jsonify({"error": "wrong password"}), 401
    else:
        from api.v1.app import auth

        user = c_user
        session_id = auth.create_session(user.id)

        SESSION_NAME = getenv("SESSION_NAME")

        response = jsonify(user.to_json())
        response.set_cookie(SESSION_NAME, session_id)

        return response


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def user_logout():
    """ used to delete the user from sesstion and
        log out the user for good.
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
