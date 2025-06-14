import pytest
from unittest.mock import patch
from app import create_app
from app.models.vehicule import Vehicle, db

@pytest.fixture(scope="function")
def client():
    app = create_app('testing')
    ctx = app.app_context()
    ctx.push()
    db.create_all()
    yield app.test_client()
    db.session.remove()
    db.drop_all()
    ctx.pop()

# Patch global : désactive la vérification JWT pour tous les tests ci-dessous
@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *a, **k: None)
def test_create_vehicule(client):
    data = {
        "registrationNumber": "ABC-123",
        "make": "Toyota",
        "model": "Corolla",
        "year": 2020,
        "rentalPrice": 20000.0
    }
    response = client.post('/vehicles', json=data)
    assert response.status_code == 201
    assert response.get_json()['message'] == "Vehicle created successfully"

@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *a, **k: None)
def test_create_vehicule_missing_fields(client): 
    data = {
        "make": "Toyota",
        "model": "Corolla"
    }
    response = client.post('/vehicles', json=data)
    assert response.status_code in [400, 500]

@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *a, **k: None)
def test_get_vehicule_not_found(client):
    response = client.get('/vehicles/9999')
    assert response.status_code == 404
    assert response.get_json()['message'] == "Vehicle not found"

@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *a, **k: None)
def test_update_vehicule_not_found(client):
    data = {
        "make": "Toyota",
        "model": "Camry",
        "year": 2021,
        "rentalPrice": 25000.0
    }
    response = client.put('/vehicles/9999', json=data)
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data is not None
    assert json_data['message'] == "Vehicle not found"


@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *a, **k: None)
def test_delete_vehicule_not_found(client):
    response = client.delete('/vehicles/9999')
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data is not None
    assert json_data['message'] == "Vehicle not found"


@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *a, **k: None)
def test_get_all_vehicules_empty(client):
    response = client.get('/vehicles')
    assert response.status_code == 200
    assert isinstance(response.get_json()['vehicles'], list)
    assert len(response.get_json()['vehicles']) == 0


# Tests complémentaires avec insertion de données

@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *a, **k: None)
def test_get_vehicule_existing(client):
    # Crée un véhicule en base
    vehicule = Vehicle(
        registrationNumber="XYZ-999",
        make="Honda",
        model="Civic",
        year=2018,
        rentalPrice=15000.0
    )
    with client.application.app_context():
        db.session.add(vehicule)
        db.session.commit()

    response = client.get(f'/vehicles/{vehicule.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['vehicle']['registrationNumber'] == "XYZ-999"
    assert data['vehicle']['make'] == "Honda"

@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *a, **k: None)
def test_update_vehicule_existing(client):
    vehicule = Vehicle(
        registrationNumber="UPD-456",
        make="Ford",
        model="Focus",
        year=2017,
        rentalPrice=13000.0
    )
    with client.application.app_context():
        db.session.add(vehicule)
        db.session.commit()

    update_data = {
        "make": "Ford",
        "model": "Fiesta",
        "year": 2019,
        "rentalPrice": 14000.0
    }
    response = client.put(f'/vehicles/{vehicule.id}', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == "Vehicle updated successfully"
    assert data['vehicle']['model'] == "Fiesta"
    assert data['vehicle']['year'] == 2019

@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *a, **k: None)
def test_delete_vehicule_existing(client):
    vehicule = Vehicle(
        registrationNumber="DEL-123",
        make="BMW",
        model="X3",
        year=2016,
        rentalPrice=28000.0
    )
    with client.application.app_context():
        db.session.add(vehicule)
        db.session.commit()

    response = client.delete(f'/vehicles/{vehicule.id}')
    assert response.status_code == 200
    assert response.get_json()['message'] == "Vehicle deleted successfully"

@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *a, **k: None)
def test_get_all_vehicules_non_empty(client):
    vehicule1 = Vehicle(
        registrationNumber="REG-001",
        make="Audi",
        model="A4",
        year=2015,
        rentalPrice=22000.0
    )
    vehicule2 = Vehicle(
        registrationNumber="REG-002",
        make="Mercedes",
        model="C-Class",
        year=2017,
        rentalPrice=35000.0
    )
    with client.application.app_context():
        db.session.add_all([vehicule1, vehicule2])
        db.session.commit()

    response = client.get('/vehicles')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data['vehicles'], list)
    assert any(v['registrationNumber'] == "REG-001" for v in data['vehicles'])
    assert any(v['registrationNumber'] == "REG-002" for v in data['vehicles'])

