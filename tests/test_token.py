import unittest
from unittest.mock import MagicMock, patch
from app import app
from faker import Faker


fake = Faker()


class TestTokenEndpoint(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch('app.routes.encode_token')
    @patch('app.routes.db.session.scalars')
    @patch('app.routes.check_password_hash')
    def test_successful_authenticate(self, mock_check_hash, mock_scalars, mock_encode_token):
        # Create a mock customer object that has an .id attribute = 123
        mock_customer = MagicMock()
        mock_customer.id = 123
        # Create a mock query object that has a first() method that will return the mock_customer
        mock_query = MagicMock()
        mock_query.first.return_value = mock_customer
        # Set the return value of the db.session.scalars() to be the mock_query
        mock_scalars.return_value = mock_query

        # Mock that the check password hash function will return True
        mock_check_hash.return_value = True

        # Mock the return value of the encode token function
        mock_encode_token.return_value = 'random.jwt.token'

        request_body = {
            "username": fake.user_name(),
            "password": fake.password()
        }

        response = self.client.post('/token', json=request_body)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['token'], 'random.jwt.token')


    def test_unauthorized_user(self):
        request_body = {
            "username": fake.user_name(),
            "password": fake.password()
        }

        response = self.client.post('/token', json=request_body)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['error'], 'Username and/or password is incorrect')
