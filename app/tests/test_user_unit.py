import pytest
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token
from app.routes.user_routes import user_bp
from app.models.user import db
from unittest.mock import patch, MagicMock


@pytest.fixture
def fake_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    JWTManager(app)
    app.register_blueprint(user_bp)

    with app.app_context():
        db.create_all()

    return app.test_client()


# --- REGISTER ROUTE ---
def test_register_success_mocked(fake_app):
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123"
    }

    with patch("app.routes.user_routes.User") as MockUser, \
         patch("app.routes.user_routes.db.session") as mock_db:

        MockUser.query.filter.return_value.first.return_value = None
        mock_user_instance = MagicMock()
        MockUser.return_value = mock_user_instance

        response = fake_app.post("/users/register", json=data)

        assert response.status_code == 201
        assert b"Utilisateur cree avec succes" in response.data


def test_register_duplicate_user_mocked(fake_app):
    data = {
        "username": "existinguser",
        "email": "existing@example.com",
        "password": "password123"
    }

    with patch("app.routes.user_routes.User") as MockUser:
        MockUser.query.filter.return_value.first.return_value = True

        response = fake_app.post("/users/register", json=data)
        assert response.status_code == 400
        assert b"Utilisateur ou email deja existant" in response.data


def test_register_with_custom_role(fake_app):
    data = {
        "username": "adminuser",
        "email": "admin@example.com",
        "password": "adminpass",
        "role": "admin"
    }

    with patch("app.routes.user_routes.User") as MockUser, \
         patch("app.routes.user_routes.db.session") as mock_db:

        MockUser.query.filter.return_value.first.return_value = None

        response = fake_app.post("/users/register", json=data)

        # ✅ Vérifie que User(...) a été appelé avec role="admin"
        MockUser.assert_called_once()
        _, kwargs = MockUser.call_args
        assert kwargs["role"] == "admin"
        assert kwargs["username"] == "adminuser"
        assert kwargs["email"] == "admin@example.com"




# --- LOGIN ROUTE ---
def test_login_success_mocked(fake_app):
    data = {
        "username": "testuser",
        "password": "password123"
    }

    with patch("app.routes.user_routes.User") as MockUser:
        mock_user = MagicMock()
        mock_user.check_password.return_value = True
        mock_user.id = 1
        MockUser.query.filter_by.return_value.first.return_value = mock_user

        response = fake_app.post("/users/login", json=data)
        assert response.status_code == 200
        assert b"access_token" in response.data


def test_login_invalid_credentials_mocked(fake_app):
    data = {
        "username": "testuser",
        "password": "wrongpassword"
    }

    with patch("app.routes.user_routes.User") as MockUser:
        mock_user = MagicMock()
        mock_user.check_password.return_value = False
        MockUser.query.filter_by.return_value.first.return_value = mock_user

        response = fake_app.post("/users/login", json=data)
        assert response.status_code == 401
        assert b"Identifiants invalides" in response.data


# --- REFRESH TOKEN ---
def test_refresh_token_generates_new_access_token(fake_app):
    with fake_app.application.app_context():
        refresh_token = create_refresh_token(identity="1")

        response = fake_app.post(
            "/users/refresh",
            headers={"Authorization": f"Bearer {refresh_token}"},
            json={}
        )
        assert response.status_code == 200
        assert b"access_token" in response.data


# --- GET /me ---
def test_get_profile_user_not_found(fake_app):
    with fake_app.application.app_context():
        access_token = create_access_token(identity="999")

        with patch("app.routes.user_routes.User.query.get", return_value=None):
            response = fake_app.get(
                "/users/me",
                headers={"Authorization": f"Bearer {access_token}"}
            )

            assert response.status_code == 404
            assert b"Utilisateur non trouve" in response.data


# --- UPDATE ---
def test_update_user_change_password_and_role(fake_app):
    with fake_app.application.app_context():
        access_token = create_access_token(identity="1")

        mock_user = MagicMock()
        mock_user.id = 1

        # Patch correctement query.get()
        with patch("app.routes.user_routes.User") as MockUser:
            MockUser.query.get.return_value = mock_user

            with patch("app.routes.user_routes.db.session.commit") as mock_commit:
                data = {
                    "username": "newname",
                    "email": "new@mail.com",
                    "password": "newpass",
                    "role": "admin"
                }

                response = fake_app.put(
                    "/users/1",
                    headers={"Authorization": f"Bearer {access_token}"},
                    json=data
                )

                assert response.status_code == 200
                mock_user.set_password.assert_called_once_with("newpass")
                assert mock_user.role == "admin"




# --- DELETE ---
def test_delete_user_success(fake_app):
    with fake_app.application.app_context():
        access_token = create_access_token(identity="1")

        mock_user = MagicMock()
        mock_user.id = 1

        # Patch proprement User.query.get
        with patch("app.routes.user_routes.User") as MockUser:
            MockUser.query.get.return_value = mock_user

            with patch("app.routes.user_routes.db.session.delete") as mock_delete, \
                 patch("app.routes.user_routes.db.session.commit"):

                response = fake_app.delete(
                    "/users/1",
                    headers={"Authorization": f"Bearer {access_token}"}
                )

                assert response.status_code == 200
                mock_delete.assert_called_once_with(mock_user)




def test_delete_user_not_found(fake_app):
    with fake_app.application.app_context():
        access_token = create_access_token(identity="1")

        with patch("app.routes.user_routes.User.query.get", return_value=None):
            response = fake_app.delete(
                "/users/999",
                headers={"Authorization": f"Bearer {access_token}"}
            )

            assert response.status_code == 404
            assert b"Utilisateur non trouve" in response.data


# --- GET ALL USERS ---
def test_get_all_users(fake_app):
    with fake_app.application.app_context():
        access_token = create_access_token(identity="1")

        mock_users = [
            MagicMock(id=1, username="user1", email="user1@mail.com", role="user"),
            MagicMock(id=2, username="user2", email="user2@mail.com", role="admin")
        ]

        with patch("app.routes.user_routes.User.query") as mock_query:
            mock_query.all.return_value = mock_users

            response = fake_app.get(
                "/users",
                headers={"Authorization": f"Bearer {access_token}"}
            )

            assert response.status_code == 200
            json_data = response.get_json()
            assert "users" in json_data
            assert len(json_data["users"]) == 2


