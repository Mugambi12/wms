# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='assets/templates', static_folder='assets/static')

    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wms.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SECRET_KEY'] = 'qwertyurioupiuodsfghfdjgkjhd2345678jgfnxdz'

    # Initialize the database with the Flask app
    db.init_app(app)
    login_manager.init_app(app)

    # Other configurations and initializations go here

    # Import blueprints
    from .backend.landing.routes import landing_bp
    from .backend.auth.routes import auth_bp
    from .backend.accounts import accounts_bp
    from .backend.accounts.accounts_context import accounts_context, inject_now

    # Register blueprints
    app.register_blueprint(landing_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(accounts_bp)

    # Register the context processor
    app.context_processor(accounts_context)
    app.context_processor(inject_now)

    # Flask-Login user loader
    from .backend.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
