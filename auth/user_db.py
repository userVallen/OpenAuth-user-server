from dotenv import load_dotenv
import os
from pymongo import MongoClient
import bcrypt

# Loads environment variables from .env
load_dotenv()
mongodb_uri = os.getenv('MONGODB_URI')

# Connect to the user database
client = MongoClient(mongodb_uri)
db = client['auth-db']

# Access the 'users' collection
users_collection = db['users']
counters_collection = db['counters']

# Function to get the next ID
def get_next_sequence(sequence_name):
    counter = db.counters.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        return_document=True,  # Return the updated document
        upsert=True  # Create the document if it doesn't exist
    )
    return counter["sequence_value"]

def create_user(name, username, password, role, email):
    # Check if user already exists
    if users_collection.find_one({"username": username}):
        return None  # User already exists

    # Get the next ID
    user_id = get_next_sequence("userid")

    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Create a new user document
    user_data = {
        "id": user_id,
        "name": name,
        "username": username,
        "password": hashed_password,
        "role": role,
        "email": email,
        "key": ""
    }

    # Insert the user into the collection
    users_collection.insert_one(user_data)
    return user_data

def verify_user(username, password):
    # Find the user by username
    user_data = users_collection.find_one({"username": username})

    if user_data is None:
        return {"status": "Not Found"}

    if bcrypt.checkpw(password.encode('utf-8'), user_data["password"]):
        return {"status": "Success", "user_data": user_data}

    return {"status": "Invalid"}
