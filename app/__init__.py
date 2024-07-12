import os
from flask import Flask # Import the Flask class from the flask library (STEP 1)
from app.database import db, migrate # Import the instance of SQLAlchemy (db) and instance of Migrate (migrate) from database module
from app.limiter import limiter
from app.caching import cache
from app.swagger_docs import swaggerui_blueprint


# Create an instance of the flask application (STEP 2)
app = Flask(__name__) # __name__ is the name of current module (when we import this, the name becomes the name of the module)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///advanced_ecommerce.db'

# Initialize the app with the flask-sqlalchemy
db.init_app(app)

# Initialize the app and db with migrate
migrate.init_app(app, db)

# Initialize the app with flask-limiter
limiter.init_app(app)

# Initialize the app with flask-caching
cache.init_app(app)

# Register the Swagger UI Blueprint
app.register_blueprint(swaggerui_blueprint)

# Import the routes file so that it runs
from . import routes, models  


# Putting routes at the bottom is a Flask specific thing. If putting at the top as customary, we will get the error: ImportError: cannot import name 'app' from partially initialized module 'app' (most likely due to a circular import) (/Users/sylver/Downloads/IT/Bootcamp/Coding Temple/Coding Temple Classes/Backend Specialization/Week 2/Day 1/FLASK-API/app/__init__.py)


# if __name__ == "__main__": # need this to run python3 app.py to start Flask
#     app.run()
