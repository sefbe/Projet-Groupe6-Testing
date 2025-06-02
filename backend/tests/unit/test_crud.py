import pytest
from app import create_app, db
from app.models import Vehicle
from app.crud import get_vehicle_by_id, create_vehicle, update_vehicle, delete_vehicle, get_all_vehicles, find_by_registration_number, find_by_price

import uuid

def unique_registration_number():
    return f"TEST-{uuid.uuid4().hex[:6].upper()}"


@pytest.fixture
def app_context():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        yield app


class TestCreateVehicle:

    def test_valid_vehicle_creation(self, app_context):
        """Boîte noire: classe d'équivalence valide"""
        reg = unique_registration_number()
        v = create_vehicle({
            "registration_number": reg,
            "make": "Toyota",
            "model": "Corolla",
            "year": 2020,
            "rental_price": 79.0
        })
        assert v.id is not None
        assert v.registration_number == reg

    def test_missing_field(self, app_context):
        """Boîte noire: champ manquant"""
        with pytest.raises(KeyError):
            reg = unique_registration_number()
            create_vehicle({
                "registration_number": reg,
                "make": "Nissan",
              # "model" is missing
                "year": 2021,
                "rental_price": 90.0
            })


    def test_invalid_year_type(self, app_context):
        """Boîte noire: valeur de type invalide"""
        with pytest.raises(ValueError):
            reg = unique_registration_number()
            create_vehicle({
                "registration_number": reg,
                "make": "Honda",
                "model": "Jazz",
                "year": "invalid-year",
                "rental_price": 80.0
            })

    def test_invalid_price_type(self, app_context):
        with pytest.raises(ValueError):
            reg = unique_registration_number()
            create_vehicle({
                "registration_number": reg,
                "make": "BMW",
                "model": "X1",
                "year": 2022,
                "rental_price": "free"  # mauvaise entrée
            })

    def test_duplicate_registration_number(self, app_context):
        """Boîte noire: violation de contrainte d’unicité"""
        reg = unique_registration_number()

        # First creation should succeed
        vehicle1 = create_vehicle({
            "registration_number": reg,
            "make": "Kia",
            "model": "Rio",
            "year": 2018,
            "rental_price": 70.0
        })
        assert vehicle1 is not None

        # Second creation with same reg should fail (returns None or custom error object)
        vehicle2 = create_vehicle({
            "registration_number": reg,
            "make": "Mazda",
            "model": "2",
            "year": 2019,
            "rental_price": 75.0
        })

        assert vehicle2 is None or getattr(vehicle2, "error", False), "Expected duplicate to fail"

    def test_year_boundaries(self, app_context):
        """Boîte noire: valeur limite (année)"""
        # minimum raisonnable
        reg = unique_registration_number()
        v = create_vehicle({
            "registration_number": reg,
            "make": "Old",
            "model": "Classic",
            "year": 1900,
            "rental_price": 30.0
        })
        assert v.year == 1900

        # maximum raisonnable
        reg = unique_registration_number()
        v = create_vehicle({
            "registration_number": reg,
            "make": "Future",
            "model": "Concept",
            "year": 2100,
            "rental_price": 200.0
        })
        assert v.year == 2100


class TestFindVehicle:

    def test_search_by_existing_registration(self, app_context):
        """Boîte blanche: chemin positif"""
        reg = unique_registration_number()
        create_vehicle({
            "registration_number": reg,
            "make": "Ford",
            "model": "Fiesta",
            "year": 2020,
            "rental_price": 90.0
        })
        v = find_by_registration_number(reg)
        assert v is not None
        assert v.make == "Ford"

    def test_search_by_non_existing_registration(self, app_context):
        """Boîte noire: classe d’équivalence inexistante"""
        reg = unique_registration_number()
        v = find_by_registration_number(reg)
        assert v is None

    def test_search_by_price_exact_match(self, app_context):
        reg = unique_registration_number()
        create_vehicle({
            "registration_number": reg,
            "make": "Audi",
            "model": "A3",
            "year": 2023,
            "rental_price": 150.0
        })
        results = find_by_price(150.0)
        assert len(results) >= 1
        assert any(v.registration_number == reg for v in results)

    def test_search_by_price_no_match(self, app_context):
        results = find_by_price(999.0)
        assert results == []


class TestUpdateVehicle:

    def test_update_model_successfully(self, app_context):
        """Boîte blanche: modification partielle"""
        reg = unique_registration_number()
        v = create_vehicle({
            "registration_number": reg,
            "make": "Peugeot",
            "model": "208",
            "year": 2020,
            "rental_price": 65.0
        })
        updated = update_vehicle(v.id, {"model": "308"})
        assert updated.model == "308"

    def test_update_with_invalid_field(self, app_context):
        """Boîte blanche: test des branches inconnues (attribut non existant)"""
        reg = unique_registration_number()
        v = create_vehicle({
            "registration_number": reg,
            "make": "Peugeot",
            "model": "2008",
            "year": 2021,
            "rental_price": 85.0
        })
        updated = update_vehicle(v.id, {"non_existent": "value"})
        # pas d’exception mais le champ n’est pas modifié
        assert not hasattr(updated, "non_existent")


class TestDeleteVehicle:

    def test_delete_existing_vehicle(self, app_context):
        """Boîte blanche: suppression OK"""
        reg = unique_registration_number()
        v = create_vehicle({
            "registration_number": reg,
            "make": "Fiat",
            "model": "500",
            "year": 2019,
            "rental_price": 60.0
        })
        delete_vehicle(v.id)
        assert get_vehicle_by_id(v.id) is None
