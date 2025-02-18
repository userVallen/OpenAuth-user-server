## Overview

This project is a part of the OpenAuth project, which is a simple OTP authentication service. This module serves as an API that handles basic requests related to a user's credentials, such as signing up (for new users) and logging in (for existing users). For more details on the OTP generation and 

## User Credentials

All of the users' credentials are stored inside a database in the following format:

```
{
    _id: ObjectId('6745677e86e463ecc4e1438f')
    id: 9
	name: "Bob"
	username: "bob"
	password: Binary.createFromBase64('JDJiJDEyJElzRG1jbDBQZVl0cUhqdDRuZjBiUmUwc0JLbjc5LjVCLjNDUWhLeXZpRi9SMjVlai4yY0Zt', 0)
	role: "user"
	email: "bob456@gmail.com"
	key: "bobServerKeyTimeComponent"
}
```
The “_id” field is a field automatically created by MongoDB to identify the document, which differs from the program’s self-generated identifier, which is the “id” field. For security reasons, all passwords stored in the database are priorly hashed with bcrypt using a specific salt. When a document has just been created, the “key” field will initially have no value (””), and will be modified once the user successfully requests for an OTP through the OTP authentication server.

## Endpoints

* /auth/signup

    The /signup endpoint creates a new document in the database after receiving an HTTP request consisting of the necessary user credentials, including name, password, role, and email, written in JSON format.
    
* /auth/login

    The /login endpoint is in charge of authenticating each login request made by clients by matching the submitted username, password, and role with what is stored in the database. A login attempt with valid credentials results in a success, an invalid username or password results in failure (user not found or invalid password respectively).

## Running the Code

- Run `app.py` to deploy the development server.
- You can now send HTTP requests to the link displayed in the terminal (e.g., http://127.0.0.1:5000).
    * Sending HTTP requests by using curl
        * Set the method to "POST".
        * Enter the URL displayed on your terminal when you run the code.
        * Set the `content-type` to `application/json` .
        * Fill in the with all of the required information in the proper JSON format.
        * Below is an example of sending an HTTP request using curl:
            ```
            curl -X POST http://127.0.0.1:5000/auth/signup \
             -H "Content-Type: application/json" \
             -d '{
                   "name": "Alice",
                   "username": "alice",
                   "password": "alice123",
                   "role": "user",
                   "email": "alice456@gmail.com"
                 }'
            ```
    * Sending HTTP requests by using Postman
        * Set the method to "POST".
        * Enter the URL displayed on your terminal when you run the code.
        * Fill in the body with all of the required information in the proper JSON format. For example:
            ```
            {
                "name": "Alice",
                "username": "alice",
                "password": "alice123",
                "role": "user",
                "email": "alice456@gmail.com"
            }
            ```
