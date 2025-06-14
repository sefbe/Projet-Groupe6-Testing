import pytest
from app import create_app
from app.models.user import User
from app.models.vehicule import Vehicle  # ✅ Import essentiel pour que la table soit créée
from flask_jwt_extended import create_access_token
from app.models import db

@pytest.fixture
def client():
    from app.models.user import User # ✅ Importe AVANT db.create_all()
    from app.models.vehicule import Vehicle

    app = create_app("testing")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = "test-key"

    with app.app_context():
        db.init_app(app)  # 👈 optionnel si déjà fait dans create_app
        db.create_all()

        # ✅ Impression de debug utile
        print("[DEBUG] Tables créées :", list(db.metadata.tables.keys()))

        yield app.test_client()

        db.session.remove()
        db.drop_all()



@pytest.fixture
def user_token(client):
    with client.application.app_context():
        user = User(username="user", email="user@test.com", role="user")
        user.set_password("userpass")
        db.session.add(user)
        db.session.commit()
        return create_access_token(identity=str(user.id))


def test_create_vehicle_success(client, user_token):
    data = {
        "registrationNumber": "ABC123",
        "make": "Toyota",
        "model": "Corolla",
        "year": 2020,
        "rentalPrice": 100.0
    }

    response = client.post(
        "/vehicles",
        headers={"Authorization": f"Bearer {user_token}"},
        json=data
    )

    assert response.status_code == 201
    assert "Vehicle created successfully" in response.get_data(as_text=True)


def test_get_all_vehicles(client, user_token):
    with client.application.app_context():
        v = Vehicle(registrationNumber="XYZ999", make="Honda", model="Civic", year=2022, rentalPrice=80.0)
        db.session.add(v)
        db.session.commit()

    response = client.get("/vehicles", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert "vehicles" in data
    assert len(data["vehicles"]) >= 1


def test_search_by_registration_success(client, user_token):
    with client.application.app_context():
        v = Vehicle(registrationNumber="REG123", make="Ford", model="Focus", year=2021, rentalPrice=90.0)
        db.session.add(v)
        db.session.commit()

    response = client.get("/vehicles/search/registration/REG123", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["registrationNumber"] == "REG123"


def test_search_by_price(client, user_token):
    with client.application.app_context():
        v = Vehicle(registrationNumber="CHEAP1", make="Fiat", model="Panda", year=2018, rentalPrice=45.0)
        db.session.add(v)
        db.session.commit()

    response = client.get("/vehicles/search/price/50.0", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(vehicle["registrationNumber"] == "CHEAP1" for vehicle in data)


def test_update_vehicle_success(client, user_token):
    with client.application.app_context():
        v = Vehicle(registrationNumber="MOD123", make="BMW", model="320", year=2015, rentalPrice=120.0)
        db.session.add(v)
        db.session.commit()
        vehicle_id = v.id

    update_data = {"model": "330", "rentalPrice": 130.0}
    response = client.put(
        f"/vehicles/{vehicle_id}",
        headers={"Authorization": f"Bearer {user_token}"},
        json=update_data
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["vehicle"]["model"] == "330"


def test_delete_vehicle_success(client, user_token):
    with client.application.app_context():
        v = Vehicle(registrationNumber="DEL123", make="Renault", model="Clio", year=2017, rentalPrice=65.0)
        db.session.add(v)
        db.session.commit()
        vehicle_id = v.id

    response = client.delete(
        f"/vehicles/{vehicle_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 200
    assert "Vehicle deleted successfully" in response.get_data(as_text=True)

def test_create_vehicle_missing_field(client, user_token):
    data = {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2020,
        "rentalPrice": 100.0
        # 🚫 "registrationNumber" manquant
    }

    response = client.post("/vehicles", headers={"Authorization": f"Bearer {user_token}"}, json=data)
    assert response.status_code == 400
    assert "Missing field" in response.get_data(as_text=True)

def test_create_vehicle_minimal_fields(client, user_token):
    data = {
        "registrationNumber": "MIN123",
        "make": "Mini",
        "model": "One",
        "year": 2023,
        "rentalPrice": 50.0
    }

    response = client.post("/vehicles", headers={"Authorization": f"Bearer {user_token}"}, json=data)
    assert response.status_code == 201


def test_create_vehicle_duplicate_registration(client, user_token):
    with client.application.app_context():
        v = Vehicle(registrationNumber="DUP123", make="Peugeot", model="208", year=2021, rentalPrice=70.0)
        db.session.add(v)
        db.session.commit()

    data = {
        "registrationNumber": "DUP123",
        "make": "Peugeot",
        "model": "2008",
        "year": 2022,
        "rentalPrice": 80.0
    }

    response = client.post("/vehicles", headers={"Authorization": f"Bearer {user_token}"}, json=data)
    assert response.status_code == 500  # ou 400 si tu gères les conflits explicitement

def test_get_vehicle_not_found(client, user_token):
    response = client.get("/vehicles/999", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 404

def test_update_vehicle_not_found(client, user_token):
    update_data = {"model": "Updated", "rentalPrice": 150.0}
    response = client.put("/vehicles/999", headers={"Authorization": f"Bearer {user_token}"}, json=update_data)
    assert response.status_code == 404

def test_delete_vehicle_not_found(client, user_token):
    response = client.delete("/vehicles/999", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 404

def test_search_by_registration_not_found(client, user_token):
    response = client.get("/vehicles/search/registration/UNKNOWN123", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 404

def test_search_by_price_no_match(client, user_token):
    response = client.get("/vehicles/search/price/10.0", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert response.get_json() == []

def test_partial_update_vehicle(client, user_token):
    with client.application.app_context():
        v = Vehicle(registrationNumber="UPD123", make="Mazda", model="3", year=2019, rentalPrice=85.0)
        db.session.add(v)
        db.session.commit()
        vid = v.id

    response = client.put(
        f"/vehicles/{vid}",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"rentalPrice": 99.0}
    )
    assert response.status_code == 200
    assert response.get_json()["vehicle"]["rentalPrice"] == 99.0

