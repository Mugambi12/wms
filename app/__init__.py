# Import necessary modules and classes

# app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configurations, database setup, and other initialization go here

    # Import blueprints
    from .auth.routes import auth_bp
    from .admin.routes import admin_bp
    from .home.routes import home_bp

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(home_bp)

    return app


