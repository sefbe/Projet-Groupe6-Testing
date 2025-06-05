import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.routes.vehicle_routes import vehicle_bp

class TestGetVehicle(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.register_blueprint(vehicle_bp)
        self.client = app.test_client()

    @patch('app.routes.vehicle_routes.Vehicle')
    def test_get_vehicle(self, mock_vehicle):
        mock_instance = MagicMock(to_dict=lambda: {"id": 1})
        mock_vehicle.query.get_or_404.return_value = mock_instance
        response = self.client.get('/vehicle/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"id": 1})

if __name__ == "__main__":
    unittest.main()

