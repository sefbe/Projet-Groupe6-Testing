import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.routes.vehicle_routes import vehicle_bp

class TestCreateVehicle(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.register_blueprint(vehicle_bp)
        self.client = app.test_client()

    @patch('app.routes.vehicle_routes.db.session')
    @patch('app.routes.vehicle_routes.Vehicle')
    def test_create_vehicle(self, mock_vehicle_class, mock_session):
        data = {
            "make": "Toyota",
            "model": "Corolla",
            "registration_number": "XYZ123",
            "rental_price": 100.0,
            "year": 2022,
            "available": True
        }
        mock_instance = MagicMock(to_dict=lambda: data)
        mock_vehicle_class.return_value = mock_instance

        response = self.client.post('/vehicle/create', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), data)

if __name__ == "__main__":
    unittest.main()

