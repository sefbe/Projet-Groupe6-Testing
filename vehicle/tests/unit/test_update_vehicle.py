import unittest
from unittest.mock import patch, MagicMock
from app import create_app

class TestUpdateVehicle(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.routes.vehicle_routes.Vehicle.query.get_or_404')
    @patch('app.routes.vehicle_routes.db.session.commit')
    def test_update_vehicle(self, mock_commit, mock_get):
        vehicle = MagicMock()
        mock_get.return_value = vehicle

        data = {
            'make': 'Toyota',
            'model': 'Corolla',
            'registration_number': 'ABC123',
            'rental_price': 75.0,
            'year': 2022,
            'available': False
        }

        # Mock the request to return the update data
        with patch('app.routes.vehicle_routes.request') as mock_request:
            mock_request.get_json.return_value = data

            # Use the test client to send a PUT request
            response = self.client.put('/vehicle/update/1')

            # Check the response status code
            self.assertEqual(response.status_code, 200)

            # Verify that the vehicle's attributes were updated
            for key, value in data.items():
                self.assertEqual(getattr(vehicle, key), value)

            mock_commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
