#!/usr/bin/env python3
"""
    a basic flask app and different end points
"""
from flask import Flask, jsonify, request, abort
from flask import redirect
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth
AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=['GET'], strict_slashes=False)
def home() -> str:
    """
        the home current page
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users() -> str:
    """
        create or return user and return the user
        that hasbeen called
    """
    email = request.form.get('email')
    passwd = request.form.get('password')

    try:
        AUTH.register_user(email, passwd)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login() -> str:
    """
        an end point used to log the user
        in and create season and log it in
    """
    email = request.form.get('email')
    passwd = request.form.get('password')

    if AUTH.valid_login(email, passwd):
        ses_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", ses_id)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """Logs out a login user and return the redirction
        to home page
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """
        this is the profile section and return json of the
        email
    """
    ses_id = request.cookies.get("session_id")
    if not ses_id:
        abort(403)
    user = AUTH.get_user_from_session_id(ses_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_password() -> str:
    """
        a toen to reset password an retur json
        with emai and reset token
    """
    email = request.form.get('email')

    try:
        AUTH._db.find_user_by(email=email)
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": "email", "reset_token": token}), 200
    except NoResultFound:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """
        a method to update password and return json format
        of the updathed things
    """
    try:
        email = request.form['email']
        reset_token = request.form['reset_token']
        new_password = request.form['new_password']
    except KeyError:
        abort(400)
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
