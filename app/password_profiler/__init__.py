from flask import Blueprint

password_profiler_bp = Blueprint('password_profiler', __name__, url_prefix='/password_profiler')

from app.password_profiler import routes