import unittest
from unittest.mock import patch, MagicMock
from app import create_app

class TestGetVehiclesByMaxPrice(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.routes.vehicle_routes.Vehicle.query.filter')
    def test_get_vehicles_by_max_price(self, mock_filter):
        # Mock vehicle instances
        vehicle1 = MagicMock()
        vehicle1.to_dict.return_value = {'rental_price': 30}
        vehicle2 = MagicMock()
        vehicle2.to_dict.return_value = {'rental_price': 40}
        
        # Mock the filter return value
        mock_query = MagicMock()
        mock_query.all.return_value = [vehicle1, vehicle2]
        mock_filter.return_value = mock_query

        # Simulate a GET request to the endpoint
        response = self.client.get('/vehicles/price/50')

        # Assert the response status code
        self.assertEqual(response.status_code, 200)
        
        # Assert the response data
        data = response.get_json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['rental_price'], 30)
        self.assertEqual(data[1]['rental_price'], 40)

if __name__ == '__main__':
    unittest.main()
