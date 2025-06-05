import unittest
from unittest.mock import patch
from flask import Flask
from app.routes.user_routes import user_bp

class TestUserRoutesIntegration(unittest.TestCase):
    def setUp(self):
        # Configure Flask app for testing
        self.app = Flask(__name__)
        self.app.register_blueprint(user_bp)
        self.client = self.app.test_client()

    @patch("app.services.user_service.UserService.create_user")
    def test_create_user(self, mock_create_user):
        mock_create_user.return_value = 1
        response = self.client.post("/users", json={
            "name": "John Doe",
            "email": "unique_email@example.com",
            "password": "password"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"id": 1})

    @patch("app.services.user_service.UserService.get_user_by_email")
    @patch("app.services.auth_service.AuthService.generate_access_token")
    @patch("app.services.auth_service.AuthService.generate_refresh_token")
    @patch("app.services.auth_service.AuthService.verify_password")
    def test_login_success(self, mock_verify_password, mock_refresh_token, mock_access_token, mock_get_user_by_email):
        mock_get_user_by_email.return_value = {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "password": "hashed_password",
            "role": "user"
        }
        mock_verify_password.return_value = True
        mock_access_token.return_value = "access_token"
        mock_refresh_token.return_value = "refresh_token"
        response = self.client.post("/login", json={
            "email": "john@example.com",
            "password": "password"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "access_token": "access_token",
            "refresh_token": "refresh_token",
            "role": "user"
        })

    @patch("app.services.user_service.UserService.update_user")
    def test_update_user(self, mock_update_user):
        mock_update_user.return_value = 1
        response = self.client.put("/users/1", json={
            "name": "John Updated",
            "email": "john_updated@example.com",
            "password": "newpassword"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "User updated"})

    @patch("app.services.user_service.UserService.update_user")
    def test_update_user_not_found(self, mock_update_user):
        mock_update_user.return_value = 0
        response = self.client.put("/users/999", json={
            "name": "Nonexistent User",
            "email": "nonexistent@example.com",
            "password": "password"
        })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "User not found"})