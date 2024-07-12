from flask_httpauth import HTTPTokenAuth
from app.utils.util import decode_token
from app.models import Customer
from app.database import db


# Create an instance of the HTTPTokenAuth class
token_auth = HTTPTokenAuth(scheme='Bearer')


@token_auth.verify_token
def verify(token):
    # Decode the token to get the customer id
    customer_id = decode_token(token)
    if customer_id is not None:
        # Get the customer with that ID
        return db.session.get(Customer, customer_id)
    else:
        return None


@token_auth.error_handler
def handle_error(status_code):
    # Getting a JSON response because it is a dictionary. Flask handles dictionaries and automatically jsonifies it (puts into Json):
    return {"error": "Invalid token. Please try again"}, status_code