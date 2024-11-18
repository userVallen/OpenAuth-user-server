from dotenv import load_dotenv
import os
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash  # For password hashing

load_dotenv()  # Loads environment variables from .env
mongodb_uri = os.getenv('MONGODB_URI')

# Connect to MongoDB
client = MongoClient(mongodb_uri)
db = client['auth-db']

# Access the 'users' collection
users_collection = db.users

def create_user(username, password):
    # Check if user already exists
    if users_collection.find_one({"username": username}):
        return None  # User already exists

    # Hash the password before storing
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Create a new user document
    user_data = {
        "username": username,
        "password": hashed_password,
        "otp": ""
    }

    # Insert the user into the collection
    users_collection.insert_one(user_data)
    return user_data

def verify_user(username, password):
    # Find the user by username
    user_data = users_collection.find_one({"username": username})
    if user_data and check_password_hash(user_data["password"], password):
        return user_data  # User is valid
    return None  # Invalid username/password