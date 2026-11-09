
from flask import Flask, request, jsonify
import logging
import re
app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
students = {}
next_id = 1

def validate_student(data):
    if not isinstance(data, dict):
        return "Invalid JSON payload"

    required = ["name", "roll_number", "email"]

    for field in required:
        if not isinstance(data.get(field), str) or not data[field].strip():
            return field + " is required"

    if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', data["email"]):
        return "Invalid email format"
    return None

@app.route('/students', methods=['POST'])
def create_student():
    global next_id

    data = request.get_json(silent=True)
    error = validate_student(data)

    if error:
        return jsonify({"error": error}), 400

    student = {
        "id": next_id,
        "name": data["name"].strip(),
        "roll_number": data["roll_number"].strip(),
        "email": data["email"].strip()
    }

    students[next_id] = student
    next_id += 1

    return jsonify(student), 201

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(list(students.values())), 200

@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    if id not in students:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(students[id]), 200
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    if id not in students:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json(silent=True)
    error = validate_student(data)

    if error:
        return jsonify({"error": error}), 400

    students[id] = {
        "id": id,
        "name": data["name"].strip(),
        "roll_number": data["roll_number"].strip(),
        "email": data["email"].strip()
    }

    return jsonify(students[id]), 200
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    if id not in students:
        return jsonify({"error": "Student not found"}), 404

    del students[id]

    return jsonify({
        "message": "Student deleted successfully"
    }), 200
@app.after_request
def log_response(response):
    app.logger.info(
        "%s %s - %s",
        request.method,
        request.path,
        response.status_code
    )
    return response
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
