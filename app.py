from flask import Flask, request, jsonify
import sqlite3
import os
from flask_cors import CORS
import jwt 
import datetime


SECRET_KEY = 'hehehe' 

app = Flask(__name__)
CORS(app) 
DB_NAME = "database.db"

# ---------- Database Initialization ----------
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS birthrate (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                latitude DECIMAL(10,5),
                longitude DECIMAL(10,5),
                value INT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mortalityrate (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                latitude DECIMAL(10,5),
                longitude DECIMAL(10,5),
                value INT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                latitude DECIMAL(10,5),
                longitude DECIMAL(10,5),
                value UNSIGNED BIG INT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sexratio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                latitude DECIMAL(10,5),
                longitude DECIMAL(10,5),
                value DECIMAL(5,3)
            )
        ''')
        conn.commit()
    print("Database initialized.")

# ---------- Helper Function ----------
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# ---------- Routes ----------
def calculate_stats(table_name):
    conn = get_db_connection()
    rows = conn.execute(f"SELECT value FROM {table_name}").fetchall()
    conn.close()

    values = [row['value'] for row in rows if row['value'] is not None]
    if not values:
        return {"average": None, "min": None, "max": None}

    return {
        "average": sum(values) / len(values),
        "min": min(values),
        "max": max(values)
    }


@app.route('/login', methods=['POST'])
def check_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
    conn.close()

    if user is None:
        return jsonify({"error": "Invalid username or password"}), 401

    payload = {
        'user_id': user['id'],
        'username': user['username'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return jsonify({
        "message": "Login successful",
        "token": token
    })


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return jsonify({"message": "User created", "user_id": cursor.lastrowid}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400
    finally:
        conn.close()


# ---------- Birthrate Endpoints ----------
@app.route('/birthrate', methods=['GET'])
def get_birthrate():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM birthrate').fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/birthrate', methods=['POST'])
def add_birthrate():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    value = data.get('value')

    if latitude is None or longitude is None or value is None:
        return jsonify({"error": "Missing data"}), 400

    conn = get_db_connection()
    conn.execute('INSERT INTO birthrate (latitude, longitude, value) VALUES (?, ?, ?)', (latitude, longitude, value))
    conn.commit()
    conn.close()
    return jsonify({"message": "Birthrate data inserted"}), 201

# ---------- Mortality Rate Endpoints ----------
@app.route('/mortalityrate', methods=['GET'])
def get_mortalityrate():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM mortalityrate').fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/mortalityrate', methods=['POST'])
def add_mortalityrate():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    value = data.get('value')

    if latitude is None or longitude is None or value is None:
        return jsonify({"error": "Missing data"}), 400

    conn = get_db_connection()
    conn.execute('INSERT INTO mortalityrate (latitude, longitude, value) VALUES (?, ?, ?)', (latitude, longitude, value))
    conn.commit()
    conn.close()
    return jsonify({"message": "Mortality rate data inserted"}), 201

# ---------- Income Endpoints ----------
@app.route('/income', methods=['GET'])
def get_income():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM income').fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/income', methods=['POST'])
def add_income():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    value = data.get('value')

    if latitude is None or longitude is None or value is None:
        return jsonify({"error": "Missing data"}), 400

    conn = get_db_connection()
    conn.execute('INSERT INTO income (latitude, longitude, value) VALUES (?, ?, ?)', (latitude, longitude, value))
    conn.commit()
    conn.close()
    return jsonify({"message": "Income data inserted"}), 201

# ---------- Sex Ratio Endpoints ----------
@app.route('/sexratio', methods=['GET'])
def get_sexratio():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM sexratio').fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/sexratio', methods=['POST'])
def add_sexratio():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    value = data.get('value')

    if latitude is None or longitude is None or value is None:
        return jsonify({"error": "Missing data"}), 400

    conn = get_db_connection()
    conn.execute('INSERT INTO sexratio (latitude, longitude, value) VALUES (?, ?, ?)', (latitude, longitude, value))
    conn.commit()
    conn.close()
    return jsonify({"message": "Sex ratio data inserted"}), 201

@app.route('/stats/mortalityrate', methods=['GET'])
def get_mortalityrate_stats():
    return jsonify(calculate_stats("mortalityrate"))

@app.route('/stats/income', methods=['GET'])
def get_income_stats():
    return jsonify(calculate_stats("income"))

@app.route('/stats/sexratio', methods=['GET'])
def get_sexratio_stats():
    return jsonify(calculate_stats("sexratio"))

@app.route('/stats/birthrate', methods=['GET'])
def get_birthrate_stats():
    return jsonify(calculate_stats("birthrate"))


# ---------- Run App ----------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)