import pytest
from app import create_app, db
from app.models.user import User
from flask_jwt_extended import create_access_token, create_refresh_token
from flask import json

@pytest.fixture
def client():
    # Crée une instance de l'application Flask pour les tests
    app = create_app('testing')  # Utilisez un environnement de test
    with app.test_client() as client:
        # Crée et retourne le client de test
        with app.app_context():
            db.create_all()  # Crée la base de données pour les tests
        yield client
        with app.app_context():
            db.drop_all()  # Nettoie la base de données après les tests

@pytest.fixture
def user(client):
    # Crée un utilisateur de test dans la base de données
    user = User(username="testuser", email="test@example.com")
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def tokens(user):
    # Crée des tokens JWT pour l'utilisateur de test
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return access_token, refresh_token

# --- Test de la route /register ---
def test_register_success(client):
    # Test de la création d'un utilisateur valide
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123"
    }
    response = client.post('/users/register', json=data)
    assert response.status_code == 201
    assert "Utilisateur créé avec succès" in response.get_data(as_text=True)

def test_register_missing_fields(client):
    # Test avec des champs manquants
    data = {
        "username": "newuser",
        "email": "newuser@example.com"
    }
    response = client.post('/users/register', json=data)
    assert response.status_code == 400
    assert "Champs manquants" in response.get_data(as_text=True)

def test_register_duplicate_user(client, user):
    # Test avec un nom d'utilisateur déjà existant
    data = {
        "username": "testuser",
        "email": "newemail@example.com",
        "password": "password123"
    }
    response = client.post('/users/register', json=data)
    assert response.status_code == 400
    assert "Utilisateur ou email déjà existant" in response.get_data(as_text=True)

# --- Test de la route /login ---
def test_login_success(client, user, tokens):
    # Test de la connexion avec des identifiants valides
    data = {
        "username": "testuser",
        "password": "password123"
    }
    response = client.post('/users/login', json=data)
    assert response.status_code == 200
    assert "access_token" in response.get_json()
    assert "refresh_token" in response.get_json()

def test_login_invalid_credentials(client):
    # Test avec des identifiants invalides
    data = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    response = client.post('/users/login', json=data)
    assert response.status_code == 401
    assert "Identifiants invalides" in response.get_data(as_text=True)

def test_login_nonexistent_user(client):
    # Test avec un utilisateur inexistant
    data = {
        "username": "nonexistentuser",
        "password": "password123"
    }
    response = client.post('/users/login', json=data)
    assert response.status_code == 401
    assert "Identifiants invalides" in response.get_data(as_text=True)

# --- Test de la route /refresh ---
def test_refresh_success(client, tokens):
    # Test pour rafraîchir un token valide
    response = client.post('/users/refresh', headers={"Authorization": f"Bearer {tokens[1]}"})
    assert response.status_code == 200
    assert "access_token" in response.get_json()

def test_refresh_invalid_token(client):
    # Test avec un token invalide
    response = client.post('/users/refresh', headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
    assert "Token invalide" in response.get_data(as_text=True)

# --- Test de la route /me ---
def test_get_profile_success(client, user, tokens):
    # Test pour récupérer le profil utilisateur avec un token valide
    response = client.get('/users/me', headers={"Authorization": f"Bearer {tokens[0]}"})
    assert response.status_code == 200
    assert "username" in response.get_json()
    assert response.get_json()["username"] == "testuser"

def test_get_profile_invalid_token(client):
    # Test avec un token invalide
    response = client.get('/users/me', headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
    assert "Token invalide" in response.get_data(as_text=True)

# --- Test de la route /users/<user_id> ---
def test_update_user_success(client, user, tokens):
    # Test pour mettre à jour un utilisateur valide
    data = {
        "username": "updateduser",
        "email": "updated@example.com"
    }
    response = client.put(f'/users/{user.id}', json=data, headers={"Authorization": f"Bearer {tokens[0]}"})
    assert response.status_code == 200
    assert "Utilisateur mis à jour" in response.get_data(as_text=True)

def test_update_user_unauthorized(client, user, tokens):
    # Test pour un utilisateur essayant de mettre à jour un autre utilisateur
    data = {
        "username": "unauthorizeduser"
    }
    response = client.put(f'/users/{user.id + 1}', json=data, headers={"Authorization": f"Bearer {tokens[0]}"})
    assert response.status_code == 403
    assert "Accès non autorisé" in response.get_data(as_text=True)

def test_update_user_not_found(client, user, tokens):
    # Test lorsque l'utilisateur n'est pas trouvé
    data = {
        "username": "nonexistentuser"
    }
    response = client.put(f'/users/{9999}', json=data, headers={"Authorization": f"Bearer {tokens[0]}"})
    assert response.status_code == 404
    assert "Utilisateur non trouvé" in response.get_data(as_text=True)

def test_update_user_invalid_email(client, user, tokens):
    # Test pour une mise à jour avec un email invalide
    data = {
        "email": "invalidemail"
    }
    response = client.put(f'/users/{user.id}', json=data, headers={"Authorization": f"Bearer {tokens[0]}"})
    assert response.status_code == 400
    assert "email" in response.get_data(as_text=True)

