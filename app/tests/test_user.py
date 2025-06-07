import pytest
from app import create_app
from app.models.user import User, db
from flask_jwt_extended import create_access_token, create_refresh_token
from flask import json

@pytest.fixture(scope="function")
def client():
    app = create_app('testing')

    ctx = app.app_context()
    ctx.push()
    db.create_all()  # 👈 Les tables sont bien créées ici
    print("[DEBUG] Tables disponibles :", db.engine.table_names())


    yield app.test_client()

    db.session.remove()
    db.drop_all()
    ctx.pop()

@pytest.fixture
def user(client):
    with client.application.app_context():
        user = User(username="testuser", email="test@mail.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
    return user  # 👈 Pas besoin de yield ici ni de suppression après test

@pytest.fixture
def two_users(client):
    with client.application.app_context():
        user1 = User(username="user1", email="user1@mail.com")
        user1.set_password("password1")
        user2 = User(username="user2", email="user2@mail.com")
        user2.set_password("password2")
        db.session.add_all([user1, user2])
        db.session.commit()
    return user1, user2



@pytest.fixture
def tokens(user):
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
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
    print("Response JSON:", response.get_json())

    assert response.status_code == 201
    assert "Utilisateur cree avec succes" in response.get_data(as_text=True)

    
def test_register_missing_fields(client):
    # Test avec des champs manquants
    data = {
        "username": "newuser",
        "email": "newuser@example.com"
    }
    response = client.post('users/register', json=data)
    assert response.status_code == 400
    assert "Champs manquants" in response.get_data(as_text=True)


def test_register_duplicate_user(client):
    # Premier utilisateur
    client.post('/users/register', json={
        "username": "testuser",
        "email": "test@mail.com",
        "password": "password123"
    })

    # Deuxième tentative avec les mêmes infos
    response = client.post('/users/register', json={
        "username": "testuser",
        "email": "test@mail.com",
        "password": "password123"
    })

    assert response.status_code == 400


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
    response = client.post('users/login', json=data)
    assert response.status_code == 401
    assert "Identifiants invalides" in response.get_data(as_text=True)

def test_login_nonexistent_user(client):
    # Test avec un utilisateur inexistant
    data = {
        "username": "nonexistentuser",
        "password": "password123"
    }
    response = client.post('users/login', json=data)
    assert response.status_code == 401
    assert "Identifiants invalides" in response.get_data(as_text=True)


# --- Test de la route /refresh ---
def test_refresh_success(client, tokens):
    refresh_token = tokens[1]
    print('\n\n\n')
    print(refresh_token)
    print('\n\n\n')
    response = client.post(
        '/users/refresh',
        headers={
            "Authorization": f"Bearer {refresh_token}",
            "Content-Type": "application/json"
        },
        json={}  # corps JSON vide obligatoire
    )
    assert response.status_code == 200


def test_refresh_invalid_token(client):
    response = client.post('/users/refresh', headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 422  # ← corrigé



# --- Test de la route /me ---
def test_get_profile_success(client, user, tokens):
    # Test pour obtenir le profil de l'utilisateur connecté
    response = client.get('/users/me', headers={"Authorization": f"Bearer {tokens[0]}"})
    assert response.status_code == 200
    data = response.get_json()
    print(data)
    assert data['username'] == user.username
    assert data['email'] == user.email



def test_get_profile_invalid_token(client):
    # Test avec un token invalide
    response = client.get('users/me', headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 422
    assert "Not enough segments" in response.get_data(as_text=True)

# --- Test de la route /users/<user_id> ---
def test_update_user_success(client, user, tokens):
    # Test pour mettre à jour un utilisateur valide
    data = {
        "username": "updateduser",
        "email": "updated@example.com"
    }
    response = client.put(f'users/{user.id}', json=data, headers={"Authorization": f"Bearer {tokens[0]}"})
    assert response.status_code == 200
    assert "Utilisateur mis a jour" in response.get_data(as_text=True)

def test_update_user_unauthorized(client, two_users):
    user1, user2 = two_users
    access_token = create_access_token(identity=str(user1.id))

    data = {"username": "unauthorizeduser"}
    response = client.put(f'/users/{user2.id}', json=data,
                          headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 403  # user1 ne peut pas modifier user2


def test_update_user_not_found(client, user, tokens):
    # Test lorsque l'utilisateur n'est pas trouvé
    data = {
        "username": "nonexistentuser"
    }
    response = client.put(f'users/{9999}', json=data, headers={"Authorization": f"Bearer {tokens[0]}"})
    assert response.status_code == 404
    assert "Utilisateur non trouve" in response.get_data(as_text=True)

def test_update_user_invalid_email(client, user, tokens):
    # Test pour une mise à jour avec un email invalide
    data = {
        "email": "invalidemail"
    }
    response = client.put(f'users/{user.id}', json=data, headers={"Authorization": f"Bearer {tokens[0]}"})
    assert response.status_code == 400
    assert "Email invalide" in response.get_data(as_text=True)


