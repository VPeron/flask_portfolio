from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Optional: Enable auto-reloading of templates during development
app.template_folder = 'templates'  # Ensure Flask knows where to find templates (default?)

# db setup and/or models update
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'  # login route

from app import routes, models

# BLUEPRINTS
# password_profiler blueprint
from app.password_profiler import password_profiler_bp  
app.register_blueprint(password_profiler_bp)
# path to the 'password_profiler/templates' directory to Jinja's search path
app.jinja_loader.searchpath.append(os.path.join(os.path.dirname(__file__), 'password_profiler', 'templates'))

# hash_calculator blueprint
from app.hash_calculator import hash_calculator_bp   
app.register_blueprint(hash_calculator_bp)
# path to the 'hash_calculator/templates' directory to Jinja's search path
app.jinja_loader.searchpath.append(os.path.join(os.path.dirname(__file__), 'hash_calculator', 'templates'))


@login_manager.user_loader
def load_user(user_id):
    from app.models import User  # importing the User model here to avoid circular imports
    return User.query.get(int(user_id))