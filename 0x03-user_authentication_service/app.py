#!/usr/bin/env python3

"""
User authentication
"""

from flask import Flask
from flask import (
    abort, jsonify,
    request, make_response, redirect
)
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Unauthorized"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def unauthorized(error) -> str:
    """Forbidden"""
    return jsonify({"error": "Forbidden"}), 403


@app.route("/")
def home() -> str:
    """Home route"""
    return "<h1>john</h1>"


@app.route('/users', methods=['POST'])
def users():
    """Register a new user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": "%s" % email, "message": "user created"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """Login a valid user"""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email=email, password=password):
        response = make_response(
            jsonify({"email": "%s" % email, "message": "logged in"}))
        response.set_cookie("sessId", AUTH.create_session(email))
        return response
    abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout():
    """Logs out a login user"""
    sessId = request.cookies.get("sessId")
    user = AUTH.get_user_from_sessId(sessId)
    if user is not None:
        AUTH.destroy_session(user.id)
        return redirect("/")
    abort(403)


@app.route("/profile")
def profile():
    """profile"""
    sessId = request.cookies.get("sessId")
    user = AUTH.get_user_from_sessId(sessId)
    if user:
        return jsonify({"email": user.email})
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
