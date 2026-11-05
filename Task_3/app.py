
from flask import Flask, request, jsonify
import sqlite3
import secrets
from functools import wraps

app = Flask(__name__)

tokens = {}

def connect_db():
    return sqlite3.connect("employees.db")

def create_table():
    con = connect_db()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary INTEGER NOT NULL
        )
    """)

    cur.execute("SELECT COUNT(*) FROM employees")
    count = cur.fetchone()[0]

    if count == 0:
        cur.execute(
            "INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)",
            ("Ali Ahmed", "IT", 50000)
        )
        cur.execute(
            "INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)",
            ("Ayesha Khan", "HR", 45000)
        )

    con.commit()
    con.close()


users = {
    "admin": {
        "password": "admin123",
        "role": "Administrator"
    },
    "employee": {
        "password": "emp123",
        "role": "Employee"
    }
}


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        token = request.headers.get("Authorization")

        if not token or not token.startswith("Bearer "):
            return jsonify({"error": "Authentication required"}), 401

        token = token.replace("Bearer ", "", 1)

        if token not in tokens:
            return jsonify({"error": "Invalid token"}), 401

        request.current_user = tokens[token]

        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if request.current_user["role"] != "Administrator":
            return jsonify({
                "error": "Access denied. Administrator only."
            }), 403

        return func(*args, **kwargs)

    return wrapper


@app.route("/login", methods=["POST"])
def login():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Username and password required"}), 400

    username = data.get("username")
    password = data.get("password")

    if username not in users or users[username]["password"] != password:
        return jsonify({"error": "Invalid username or password"}), 401

    token = secrets.token_hex(16)

    tokens[token] = {
        "username": username,
        "role": users[username]["role"]
    }

    return jsonify({
        "message": "Login successful",
        "username": username,
        "role": users[username]["role"],
        "token": token
    }), 200


@app.route("/employees", methods=["GET"])
@token_required
def get_employees():

    con = connect_db()
    cur = con.cursor()

    cur.execute("SELECT * FROM employees")
    rows = cur.fetchall()

    con.close()

    employees = []

    for row in rows:
        employees.append({
            "id": row[0],
            "name": row[1],
            "department": row[2],
            "salary": row[3]
        })

    return jsonify(employees), 200


@app.route("/employees", methods=["POST"])
@token_required
@admin_required
def add_employee():

    data = request.get_json(silent=True)

    if not data or not all(data.get(field) is not None for field in ["name", "department", "salary"]):
        return jsonify({"error": "Name, department and salary are required"}), 400

    con = connect_db()
    cur = con.cursor()

    cur.execute(
        "INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)",
        (data["name"], data["department"], data["salary"])
    )

    con.commit()
    employee_id = cur.lastrowid
    con.close()

    return jsonify({
        "message": "Employee added successfully",
        "id": employee_id
    }), 201


@app.route("/employees/<int:id>", methods=["PUT"])
@token_required
@admin_required
def update_employee(id):

    data = request.get_json(silent=True)

    if not data or not all(data.get(field) is not None for field in ["name", "department", "salary"]):
        return jsonify({"error": "Name, department and salary are required"}), 400

    con = connect_db()
    cur = con.cursor()

    cur.execute(
        "UPDATE employees SET name=?, department=?, salary=? WHERE id=?",
        (data["name"], data["department"], data["salary"], id)
    )

    con.commit()
    changed = cur.rowcount
    con.close()

    if changed == 0:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify({"message": "Employee updated successfully"}), 200


@app.route("/employees/<int:id>", methods=["DELETE"])
@token_required
@admin_required
def delete_employee(id):

    con = connect_db()
    cur = con.cursor()

    cur.execute("DELETE FROM employees WHERE id=?", (id,))

    con.commit()
    changed = cur.rowcount
    con.close()

    if changed == 0:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify({"message": "Employee deleted successfully"}), 200


if __name__ == "__main__":
    create_table()
    app.run(debug=True, port=5002, use_reloader=False)
