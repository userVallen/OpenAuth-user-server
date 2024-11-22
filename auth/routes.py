from flask import Blueprint, request, jsonify
from auth.user_db import create_user, verify_user

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')

    # Call the create_user function to add the user
    user_data = create_user(name, username, password)
    if user_data is None:
        return jsonify({"message": "User already exists!"}), 400

    return jsonify({"message": "User created successfully!"}), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Call the verify_user function to check credentials
    user_data = verify_user(username, password)
    if user_data is None:
        return jsonify({"message": "Invalid username or password"}), 401

    return jsonify({"message": "Login successful!"}), 200