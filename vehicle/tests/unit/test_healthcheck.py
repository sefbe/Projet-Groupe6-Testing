import unittest
from flask import Flask
from app.routes.vehicle_routes import vehicle_bp

class TestHealthcheck(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.register_blueprint(vehicle_bp)
        self.client = app.test_client()

    def test_healthcheck(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "OK"})

if __name__ == "__main__":
    unittest.main()

