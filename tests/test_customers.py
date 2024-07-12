import unittest
from unittest.mock import MagicMock, patch
from app import app



class TestCustomersEndpoint(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_get_customers(self):
        response = self.app.get('/customers')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

