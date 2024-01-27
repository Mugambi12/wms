# app/__init__.py

from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configurations, database setup, and other initialization go here

    # Import blueprints
    from .landing.routes import landing_bp
    from .auth.routes import auth_bp
    from .accounts.routes import accounts_bp
    from .accounts import accounts_context

    # Register blueprints
    app.register_blueprint(landing_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(accounts_bp)

    # Register the context processor
    app.context_processor(accounts_context)

    return app
