import unittest
from unittest.mock import patch, MagicMock
from app.services.user_service import UserService
from app.services.auth_service import AuthService

class TestUserService(unittest.TestCase):

    @patch("app.services.auth_service.AuthService.hash_password")
    @patch("app.models.user_model.User")
    @patch("app.services.user_service.db")
    def test_create_user(self, mock_db, mock_user_model, mock_hash_password):
        # Mock le hachage du mot de passe
        mock_hash_password.return_value = "hashed_password"

        # Mock le modèle User et la base de données
        mock_user_instance = MagicMock()
        mock_user_instance.id = 1
        mock_user_model.return_value = mock_user_instance

        # Appeler la fonction
        user_id = UserService.create_user("John Doe", "unique_email@example.com", "password", role="user")

        # Vérifier les assertions
        self.assertEqual(user_id, 1)
        mock_hash_password.assert_called_once_with("password")
        mock_user_model.assert_called_once_with(
            name="John Doe",
            email="unique_email@example.com",
            password="hashed_password",
            role="user"
        )
        mock_db.session.add.assert_called_once_with(mock_user_instance)
        mock_db.session.commit.assert_called_once()

    @patch("app.models.user_model.User")
    def test_get_user_by_email(self, mock_user_model):
        # Mock le modèle User
        mock_user_instance = MagicMock()
        mock_user_instance.to_dict.return_value = {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "role": "user"
        }
        mock_user_model.query.filter_by.return_value.first.return_value = mock_user_instance

        # Appeler la fonction
        user = UserService.get_user_by_email("john@example.com")

        # Vérifier les assertions
        self.assertIsNotNone(user)
        self.assertEqual(user["id"], 1)
        self.assertEqual(user["email"], "john@example.com")
        self.assertEqual(user["role"], "user")
        mock_user_model.query.filter_by.assert_called_once_with(email="john@example.com")

    @patch("app.services.auth_service.AuthService.hash_password")
    @patch("app.models.user_model.User")
    @patch("app.services.user_service.db")
    def test_update_user(self, mock_db, mock_user_model, mock_hash_password):
        # Mock le hachage du mot de passe
        mock_hash_password.return_value = "hashed_new_password"

        # Mock le modèle User
        mock_user_instance = MagicMock()
        mock_user_model.query.get.return_value = mock_user_instance

        # Appeler la fonction
        rows_affected = UserService.update_user(1, "John Updated", "john_updated@example.com", "newpassword")

        # Vérifier les assertions
        self.assertEqual(rows_affected, 1)
        mock_hash_password.assert_called_once_with("newpassword")
        self.assertEqual(mock_user_instance.name, "John Updated")
        self.assertEqual(mock_user_instance.email, "john_updated@example.com")
        self.assertEqual(mock_user_instance.password, "hashed_new_password")
        mock_db.session.commit.assert_called_once()

        # Cas où l'utilisateur n'existe pas
        mock_user_model.query.get.return_value = None
        rows_affected = UserService.update_user(2, "Jane Doe", "jane@example.com", "password")
        self.assertEqual(rows_affected, 0)