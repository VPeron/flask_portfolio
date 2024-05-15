from flask import Blueprint

hash_calculator_bp = Blueprint('hash_calculator', __name__, url_prefix='/hash_calculator')

from app.hash_calculator import routes