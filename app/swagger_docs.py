from flask_swagger_ui import get_swaggerui_blueprint


SWAGGER_URL = '/api/docs' # URL for exposing Swagger UI
API_URL = '/static/swagger.yaml' # Path to the YAML file describing UI

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name': 'Coding Temple E-Commerce'
    }
)