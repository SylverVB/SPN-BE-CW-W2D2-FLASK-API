from app import app, db, limiter, cache # from the app folder, import the app variable (Flask instance)
from flask import request, redirect, url_for
from app.schemas.customerSchema import customer_input_schema, customer_output_schema, customers_schema, customer_login_schema
from app.schemas.productSchema import product_schema, products_schema
from marshmallow import ValidationError
# from app.database import db   # imported from app instead
from app.models import Customer, Product
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.util import encode_token
from app.auth import token_auth

# Before redirection
# @app.route('/')
# # @token_auth.login_required
# def index():
#     return 'Goodbye'

# Redirecting our home page to API documentation
@app.route('/')
def index():
    return redirect(url_for('swagger_ui.show'))

# Using a database, no longer need it:
# customers = [
#     {
#         "id": 1,
#         "first_name": "Brian",
#         "last_name": "Stanton",
#         "username": "brians",
#         "email": "brians@codingtemple.com",
#         "password": "abc123",
#     },
#     {
#         "id": 2,
#         "first_name": "Ryan",
#         "last_name": "Rhoades",
#         "username": "ryanr",
#         "email": "ryanr@codingtemple.com",
#         "password": "cba321"
#     },
# ]

# Token Route
@app.route('/token', methods=["POST"])
def get_token():
    if not request.is_json:
        return {"error": "Request body must be application/json"}, 400 # Bad Request by Client
    try:
        # Verify the request data
        data = request.json
        credentials = customer_login_schema.load(data)
        # Query the customer table for a customer with that username
        query = db.select(Customer).where(Customer.username==credentials['username'])
        customer = db.session.scalars(query).first()
        # If is is a customer and the customer's password matches the credentials
        if customer is not None and check_password_hash(customer.password, credentials['password']):
            # Generate a token with the customer's id
            auth_token = encode_token(customer.id)
            return {'token': auth_token}, 200
        # If either the customer with that username does not exist or the password is wrong
        else:
            return {"error": "Username and/or password is incorrect"}, 401 # Unauthorized
    except ValidationError as err:
        return err.messages, 400

# Customer Routes

# Get all customers
@app.route('/customers', methods=['GET'])
@cache.cached(timeout=60) # Storing the data in cache for 60 seconds for faster accesses, we don't need to always access server for information. It also    means that for 60 seconds the function get_all_customers() is not being run because of cached data
def get_all_customers():
    # Get the query parameters from the request
    # print('This get_all_customers function is running')
    args = request.args
    page = args.get('page', 1, type=int)
    per_page = args.get('per_page', 10, type=int)
    search = args.get('search', '')
    query = db.select(Customer).where(Customer.username.like(f'%{search}%')).limit(per_page).offset((page-1)*per_page)
    customers = db.session.scalars(query).all()

    # return customers # before schemas
    # query = db.select(Customer) # select the Customer model # before pagination
    # customers = db.session.execute(query).scalars().all() # before pagination

    return customers_schema.jsonify(customers)

# Get a single customer by ID
@app.route('/customers/<int:customer_id>', methods=["GET"])
def get_single_customer(customer_id):
    # # Search for a customer with that ID
    # for customer in customers:
    #     if customer['id'] == customer_id:
            # return customer # was before we added schemas
    # Search the database for a customer with that ID
    customer = db.session.get(Customer, customer_id)
    # Check if we get a customer back or None
    if customer is not None:
        return customer_output_schema.jsonify(customer)
    return {"error": f"Customer with ID {customer_id} does not exist"}, 404 # Not Found

# Create a new customer
@app.route('/customers', methods=["POST"])
def create_customer():
    # Check if the request has a JSON body
    if not request.is_json:
        return {"error": "Request body must be application/json"}, 400 # Bad Request by Client
    try:
        # Get the request JSON body
        data = request.json
        # Check if the body has all of the required fields
        customer_data = customer_input_schema.load(data)
        # Before schema (Day 1):
        # required_fields = ["first_name", "last_name", "username", "email"]
        # for field in required_fields:
        #     if field not in data:
        #         return {"error": f"{field} is required to create a customer"}, 400
        # Add the data (with a new id) to the customers list
        # data["id"] = len(customers) + 1
        # customers.append(data)

        # Removed on Day 2:
        # Add the data (with a new id) to the customers list
        # customer_data["id"] = len(customers) + 1
        # customers.append(customer_data)

        # Query the customer table to see if any customers have that username or email
        query = db.select(Customer).where( (Customer.username == customer_data['username']) | (Customer.email == customer_data['email']) )
        check_customers = db.session.scalars(query).all()
        if check_customers: # If there are customers in the check_customers list (empty list evaluates to false)
            return {"error": "Customer with that username and/or email already exists"}, 400 # Bad Request by Client

        # Create a new instance of Customer 
        new_customer = Customer(
            first_name=customer_data['first_name'],
            last_name=customer_data['last_name'],
            username=customer_data['username'],
            email=customer_data['email'],
            password=generate_password_hash(customer_data['password'])
        )
        # and add to the database
        db.session.add(new_customer)
        db.session.commit()

        # return data, 201 # Created - Success (with this we get password)
        
        # Serialize the new customer object and return with 201 status
        return customer_output_schema.jsonify(new_customer), 201 # Created - Success
    except ValidationError as err:
        return err.messages, 400
    except ValueError as err:
        return {"error": str(err)}, 400


# Product Endpoints 

# Get all products
@app.route('/products', methods=["GET"])
@limiter.limit("50 per hour")
def get_all_products():
    # Get any request query params aka request.args
    args = request.args
    page = args.get('page', 1, type=int)
    # print(f"The page arg is: {page} and the data type is {type(page)}")
    per_page = args.get('per_page', 10, type=int)
    # print(page, per_page)
    search = args.get('search', '')
    # query = db.select(Product) # before pagination
    # Query the database for products and limit and offset based on the query params
    query = db.select(Product).where(Product.name.like(f'%{search}%')).limit(per_page).offset((page-1)*per_page)
    products = db.session.scalars(query).all()
    return products_schema.jsonify(products)   

# Get a single product by ID
@app.route('/products/<int:product_id>', methods=["GET"])
def get_single_product(product_id):
    # Search the database for a product with that ID
    product = db.session.get(Product, product_id)
    # Check if we get a customer back or None
    if product is not None:
        return product_schema.jsonify(product)
    return {"error": f"Product with ID {product_id} does not exist"}, 404 # Not Found

# Create a new product and store in db
@app.route('/products', methods=["POST"])
@token_auth.login_required
def create_product():
    logged_in_user = token_auth.current_user()
    print(f'{logged_in_user} is creating a new product')
    # Check if the request has a JSON body
    if not request.is_json:
        return {"error": "Request body must be application/json"}, 400 # Bad Request by Client
    try:
        # Get the JSON body from the request
        raw_data = request.json
        # Validate the data using our product schema
        product_data = product_schema.load(raw_data)
        # # If our products unique:
        # product_exists = db.session.execute(db.select(Product).where(Product.name == product_data['name'])).scalars().one()
        # if product_exists:
        #     return {'error': "That product already exists"}
        # Create a new instance of the Product class
        new_product = Product(name=product_data['name'], price=product_data['price'])
        # Add the new product to the database
        db.session.add(new_product)
        db.session.commit()
        return product_schema.jsonify(new_product), 201 # Created
    except ValidationError as err:
        return err.messages, 400 # Bad Request by client