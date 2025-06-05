import unittest
from unittest.mock import patch, MagicMock
from app import create_app

class TestDeleteVehicle(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.routes.vehicle_routes.Vehicle.query.get_or_404')
    @patch('app.routes.vehicle_routes.db.session.delete')
    @patch('app.routes.vehicle_routes.db.session.commit')
    def test_delete_vehicle_success(self, mock_commit, mock_delete, mock_get):
        # Mock vehicle instance
        vehicle = MagicMock()
        mock_get.return_value = vehicle

        # Simulate a DELETE request
        response = self.client.delete('/vehicle/delete/1')

        # Check the response status code
        self.assertEqual(response.status_code, 200)
        mock_delete.assert_called_once_with(vehicle)
        mock_commit.assert_called_once()

    @patch('app.routes.vehicle_routes.Vehicle.query.get_or_404')
    def test_delete_vehicle_not_found(self, mock_get):
        # Simulate a not found scenario
        mock_get.side_effect = Exception("Not Found")

        # Simulate a DELETE request
        response = self.client.delete('/vehicle/delete/1')

        # Check the response status code
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
