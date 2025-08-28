# app.py
from flask import Flask, request, jsonify

app = Flask(__name__)

APP_VERSION = "1.1.5"

@app.route("/health")
def health():
    return jsonify(status="ok"), 200     

@app.route("/")
def home():
    return f"Hello from Without zero dwontime method App! Version: {APP_VERSION}"

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "123":
        return jsonify({"message": "Login success", "version": APP_VERSION, "token": "12345678"})
    return jsonify({"message": "Invalid credentials", "version": APP_VERSION}), 401

@app.route("/order", methods=["POST"])
def order():
    data = request.get_json()
    token = request.headers.get("Authorization")
    orderData = data.get("order")
    if token == "12345678":
        return jsonify({"message": "Succes post order", "order": orderData})
    return jsonify({"message": "invalid token"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
