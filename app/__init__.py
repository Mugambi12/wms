# app/__init__.py

from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configurations, database setup, and other initialization go here

    # Import blueprints
    from .landing.routes import home_bp
    from .auth.routes import auth_bp
    from .accounts.routes import dashboard_bp
    from .accounts import dashboard_context

    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    # Register the context processor
    app.context_processor(dashboard_context)

    return app
