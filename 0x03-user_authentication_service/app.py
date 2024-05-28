#!/usr/bin/env python3
"""
    a basic flask app
"""
from flask import Flask
from flask import jsonify
from flask import request
from auth import Auth
Auth = Auth()
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
        Auth.register_user(email, passwd)
        return jsonify({"email": f"{email}", "message": "user created"}), 400
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
