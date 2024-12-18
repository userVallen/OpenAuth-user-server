from flask import Blueprint, request, jsonify
from auth.user_db import create_user, verify_user

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    email = data.get('email')

    # Call the create_user function to add the user
    status = create_user(name, username, password, role, email)
    if status is None:
        return jsonify({"message": "User already exists!"}), 400

    return jsonify({"message": "User created successfully!"}), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    # Call the verify_user function to check credentials
    result = verify_user(username, password, role)
    if result['status'] == "Invalid":
        return jsonify({"message": "Invalid password"}), 401

    if result['status'] == "Mismatch":
        return jsonify({"message": "Incorrect role"}), 401

    if result['status'] == "Not Found":
        return jsonify({"message": "User not found"}), 404

    return jsonify({"message": "Login successful!"}), 200