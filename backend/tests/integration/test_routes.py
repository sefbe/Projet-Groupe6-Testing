import requests
import uuid

BASE_URL = "http://localhost:5000/vehicles"

def unique_reg():
    return f"REG{uuid.uuid4().hex[:6].upper()}"

class TestCreateVehicle:

    def test_create_valid_vehicle(self):
        reg = unique_reg()
        res = requests.post(BASE_URL, json={
            "registration_number": reg,
            "make": "Renault",
            "model": "Captur",
            "year": 2022,
            "rental_price": 95.0
        })
        assert res.status_code == 201
        data = res.json()
        assert data["registration_number"] == reg

    def test_create_missing_field(self):
        reg = unique_reg()
        res = requests.post(BASE_URL, json={
            "registration_number": reg,
            "make": "Peugeot",
            # Missing model
            "year": 2022,
            "rental_price": 90.0
        })
        assert res.status_code in (400, 500)

    def test_create_duplicate_registration(self):
        reg = unique_reg()
        requests.post(BASE_URL, json={
            "registration_number": reg,
            "make": "Mazda",
            "model": "CX5",
            "year": 2021,
            "rental_price": 110.0
        })
        res = requests.post(BASE_URL, json={
            "registration_number": reg,
            "make": "Mazda",
            "model": "CX3",
            "year": 2021,
            "rental_price": 105.0
        })
        assert res.status_code in (400, 409, 500)


class TestGetVehicle:

    def test_get_existing_vehicle_by_id(self):
        reg = unique_reg()
        post = requests.post(BASE_URL, json={
            "registration_number": reg,
            "make": "Nissan",
            "model": "Juke",
            "year": 2020,
            "rental_price": 85.0
        })
        v_id = post.json()["id"]
        res = requests.get(f"{BASE_URL}/{v_id}")
        assert res.status_code == 200
        assert res.json()["registration_number"] == reg

    def test_get_nonexistent_vehicle(self):
        res = requests.get(f"{BASE_URL}/999999")
        assert res.status_code == 404


class TestSearch:

    def test_search_by_registration(self):
        reg = unique_reg()
        requests.post(BASE_URL, json={
            "registration_number": reg,
            "make": "Citroën",
            "model": "C4",
            "year": 2021,
            "rental_price": 88.0
        })
        res = requests.get(f"{BASE_URL}/search/registration?reg={reg}")
        assert res.status_code == 200
        assert res.json()["make"] == "Citroën"

    def test_search_by_price(self):
        reg = unique_reg()
        requests.post(BASE_URL, json={
            "registration_number": reg,
            "make": "Ford",
            "model": "Focus",
            "year": 2020,
            "rental_price": 77.0
        })
        res = requests.get(f"{BASE_URL}/search/price?price=77.0")
        assert res.status_code == 200
        assert any(v["registration_number"] == reg for v in res.json())


class TestUpdate:

    def test_update_vehicle_model(self):
        reg = unique_reg()
        post = requests.post(BASE_URL, json={
            "registration_number": reg,
            "make": "VW",
            "model": "Polo",
            "year": 2019,
            "rental_price": 70.0
        })
        v_id = post.json()["id"]
        res = requests.put(f"{BASE_URL}/{v_id}", json={"model": "Golf"})
        assert res.status_code == 200
        assert res.json()["model"] == "Golf"


class TestDelete:

    def test_delete_vehicle(self):
        reg = unique_reg()
        post = requests.post(BASE_URL, json={
            "registration_number": reg,
            "make": "Skoda",
            "model": "Fabia",
            "year": 2021,
            "rental_price": 75.0
        })
        v_id = post.json()["id"]
        res = requests.delete(f"{BASE_URL}/{v_id}")
        assert res.status_code == 204

        # Vérifie qu'il est bien supprimé
        res2 = requests.get(f"{BASE_URL}/{v_id}")
        assert res2.status_code == 404
