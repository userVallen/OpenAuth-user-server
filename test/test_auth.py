import unittest
from flask import Flask
from auth.routes import auth_blueprint
from auth.user_db import users_collection

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        # Create a Flask app for testing
        self.app = Flask(__name__)
        self.app.register_blueprint(auth_blueprint, url_prefix='/auth')
        self.client = self.app.test_client()

        # Use the testing configuration to avoid affecting the real database
        self.app.config['TESTING'] = True

        # Clear the test database collection before each test
        users_collection.delete_many({})

    def tearDown(self):
        # Clean up the database after each test
        users_collection.delete_many({})

    def test_signup_success(self):
        # Test successful user signup
        response = self.client.post('/auth/signup', json={
            'name': 'Test User',
            'username': 'testuser',
            'password': 'testuser123'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User created successfully!', response.get_json().get('message'))

    def test_signup_duplicate_username(self):
        # Test signup with an already existing username
        self.client.post('/auth/signup', json={
            'name': 'Test User',
            'username': 'testuser',
            'password': 'testuser123'
        })

        # Attempt to signup with the same username
        response = self.client.post('/auth/signup', json={
            'name': 'Test User',
            'username': 'testuser',
            'password': 'testuser123'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('User already exists!', response.get_json().get('message'))

    def test_login_success(self):
        # Create a user for login test
        self.client.post('/auth/signup', json={
            'name': 'Test User',
            'username': 'testuser',
            'password': 'testuser123'
        })

        # Test successful login
        response = self.client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'testuser123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login successful!', response.get_json().get('message'))

    def test_login_invalid_credentials(self):
        # Create a user for invalid login test
        self.client.post('/auth/signup', json={
            'name': 'Test User',
            'username': 'testuser',
            'password': 'testuser123'
        })

        # Test login with incorrect password
        response = self.client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid username or password', response.get_json().get('message'))


if __name__ == '__main__':
    unittest.main()
