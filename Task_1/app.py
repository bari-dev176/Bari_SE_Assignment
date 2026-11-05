
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def connect_db():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = connect_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/students", methods=["GET"])
def get_students():
    conn = connect_db()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return jsonify([dict(row) for row in students])

@app.route("/students/<int:id>", methods=["GET"])
def get_student(id):
    conn = connect_db()
    student = conn.execute(
        "SELECT * FROM students WHERE id=?", (id,)
    ).fetchone()
    conn.close()

    if student:
        return jsonify(dict(student))
    return jsonify({"message": "Student not found"}), 404

@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()

    if not data or not all(k in data for k in ["id", "name", "department", "email"]):
        return jsonify({"message": "All fields are required"}), 400

    try:
        conn = connect_db()
        conn.execute(
            "INSERT INTO students VALUES (?, ?, ?, ?)",
            (data["id"], data["name"], data["department"], data["email"])
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Student added successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"message": "Student ID already exists"}), 409

@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.get_json()

    if not data or not all(k in data for k in ["name", "department", "email"]):
        return jsonify({"message": "All fields are required"}), 400

    conn = connect_db()
    cursor = conn.execute(
        "UPDATE students SET name=?, department=?, email=? WHERE id=?",
        (data["name"], data["department"], data["email"], id)
    )
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"message": "Student not found"}), 404

    return jsonify({"message": "Student updated successfully"})

@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    conn = connect_db()
    cursor = conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"message": "Student not found"}), 404

    return jsonify({"message": "Student deleted successfully"})

if __name__ == "__main__":
    create_table()
    app.run(debug=True, port=5000)
