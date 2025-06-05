import unittest
from unittest.mock import patch, MagicMock
from app import create_app  # importe ta factory Flask

class TestGetVehicles(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.routes.vehicle_routes.Vehicle')
    def test_get_vehicles(self, mock_vehicle):
        mock_vehicle.query.all.return_value = [MagicMock(to_dict=lambda: {"id": 1})]

        response = self.client.get('/vehicles')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [{"id": 1}])

if __name__ == "__main__":
    unittest.main()
