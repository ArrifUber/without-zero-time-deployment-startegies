# app.py
from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)
DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin1234")
DB_NAME = os.getenv("DB_NAME", "mydb")

APP_VERSION = "1.1.6"

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@app.route("/health")
def health():
    return jsonify(status="ok"), 200     

@app.route("/")
def home():
    return f"Hello from Rolling App! Version: {APP_VERSION}"

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
    ordersData = data.get("order")

    if token == "12345678":
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            item_id INT,
            price DECIMAL(10,2),
            quantity INT,
            total_price DECIMAL(10,2)
            )
        ''')

        
        for o in ordersData:
            item_id = o.get("item_id")
            price = o.get("price")
            quantity = o.get("quantity")
            total_price = o.get("total_price")

            cursor.execute(
                "INSERT INTO orders (item_id, price, quantity, total_price) VALUES (%s, %s, %s, %s)",
                (item_id, price, quantity, total_price)
            )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Succes post order", "order": ordersData})
    return jsonify({"message": "invalid token"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
