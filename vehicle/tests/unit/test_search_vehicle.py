import unittest
from unittest.mock import patch, MagicMock
from app import create_app

class TestSearchVehicleByRegistration(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()  # Active le contexte d'application
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()  # Désactive le contexte d'application

    @patch('app.routes.vehicle_routes.Vehicle.query.filter_by')  # Chemin corrigé
    def test_search_vehicle_found(self, mock_filter):
        vehicle = MagicMock()
        vehicle.to_dict.return_value = {'registration_number': 'ABC123'}
        mock_filter.return_value.first.return_value = vehicle

        response = self.client.get('/vehicle/search/ABC123')

        mock_filter.assert_called_once_with(registration_number='ABC123')
        self.assertEqual(response.status_code, 200)
        self.assertIn('registration_number', response.get_json())

    @patch('app.routes.vehicle_routes.Vehicle.query.filter_by')  # Chemin corrigé
    def test_search_vehicle_not_found(self, mock_filter):
        mock_filter.return_value.first.return_value = None

        response = self.client.get('/vehicle/search/XYZ999')

        mock_filter.assert_called_once_with(registration_number='XYZ999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Vehicle not found', response.get_json()['message'])

if __name__ == '__main__':
    unittest.main()