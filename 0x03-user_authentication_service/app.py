#!/usr/bin/env python3
"""
    a basic flask app
"""
from flask import Flask, jsonify, request, abort
from flask import redirect
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth
AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=['GET'], strict_slashes=False)
def home() -> str:
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users() -> str:
    """
        create or return user
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
        in
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
    """Logs out a login user
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is not None:
        AUTH.destroy_session(user.id)
        return redirect("/")
    abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """
        this is the profile section
    """
    ses_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(ses_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)

@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_password() -> str:
    """
        a toen to reset password
    """
    email = request.form.get('email')

    try:
        AUTH._db.find_user_by(email=email)
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": "email", "reset_token": token}), 200
    except NoResultFound:
        abort(403)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
