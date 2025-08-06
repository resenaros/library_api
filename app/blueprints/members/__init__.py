from flask import Blueprint

members_bp = Blueprint('members_bp', __name__)

from . import routes  # Import routes to register them with the blueprint