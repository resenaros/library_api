from flask import Blueprint

items_bp = Blueprint('items_bp', __name__)

from . import routes  # Import routes to register them with the blueprint