from dotenv import load_dotenv
import os
from pymongo import MongoClient
import bcrypt

load_dotenv()  # Loads environment variables from .env

# Connect to the user database
mongodb_uri = os.getenv('MONGODB_URI')
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

def create_user(name, username, password):
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
        "role": "",
        "key": ""
    }

    # Insert the user into the collection
    users_collection.insert_one(user_data)
    return user_data

def verify_user(username, password):
    # Find the user by username
    user_data = users_collection.find_one({"username": username})
    # if user_data and check_password_hash(user_data["password"], password):
    #     return user_data  # User is valid
    # return None  # Invalid username/password

    if bcrypt.checkpw(password.encode('utf-8'), user_data["password"]):
        return user_data
    return None