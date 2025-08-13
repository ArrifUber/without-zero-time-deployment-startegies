# app.py
from flask import Flask, request, jsonify
import time
from datetime import datetime
app = Flask(__name__)

APP_VERSION = "1.0.1"

@app.route("/")
def home():
    return f"Hello from Zero Downtime App! Version: {APP_VERSION}"

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "123":
        return jsonify({"message": "Login success", "version": APP_VERSION})
    return jsonify({"message": "Invalid credentials", "version": APP_VERSION}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
