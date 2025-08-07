from flask import Flask, app
from .extensions import ma, limiter, cache
from .models import db
from .blueprints.members import members_bp
from .blueprints.loans import loans_bp
from .blueprints.books import books_bp
from .blueprints.items import items_bp
from .blueprints.orders import orders_bp
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint

migrate = Migrate()

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.yaml'  # Our API URL (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Your API's Name"
    }
)

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Load app configuration
    if config_name:
        app.config.from_object(f"config.{config_name}")
    else:
        app.config.from_object("config.DevelopmentConfig")
    
    #initialize extensions
    db.init_app(app)  # adding our db extension to our app
    ma.init_app(app)  # adding our marshmallow extension to our app
    limiter.init_app(app)  # adding our limiter extension to our app
    cache.init_app(app)  # adding our cache extension to our app
    migrate.init_app(app, db)  # adding our migration extension to our app

    #Register blueprints
    app.register_blueprint(members_bp, url_prefix='/members')
    app.register_blueprint(loans_bp, url_prefix='/loans')
    app.register_blueprint(books_bp, url_prefix='/books')
    app.register_blueprint(items_bp, url_prefix='/items')
    app.register_blueprint(orders_bp, url_prefix='/orders')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL) # Register Swagger UI blueprint

    return app
    