from flask import Blueprint

orders_bp = Blueprint('orders_bp', __name__)

from . import routes  # Import routes to register them with the blueprint