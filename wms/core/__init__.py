import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import generate_csrf
from flask_apscheduler import APScheduler
from flask_mail import Mail

from config import MailConfig, DevelopmentConfig, ProductionConfig
from .utils import format_amount


db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')

    app.config.from_object(ProductionConfig)

    uploads_folder = os.path.join(app.root_path, 'frontend', 'static', 'uploads', 'profile')
    os.makedirs(uploads_folder, exist_ok=True)
    tmp_folder = os.path.join(app.root_path, 'frontend', 'static', 'uploads', 'tmp')
    os.makedirs(tmp_folder, exist_ok=True)


    with app.app_context():
        db.init_app(app)
        login_manager.init_app(app)
        login_manager.login_view = 'auth.login'

        from core.backend.accounts.components.payment_processor import process_payments_with_context
        scheduler = APScheduler()
        scheduler.init_app(app)
        scheduler.add_job(id='process_payments', func=process_payments_with_context, trigger='interval', hours=6)
        scheduler.start()

        from .backend.landing.routes import landing_bp
        from .backend.auth.routes import auth_bp
        from .backend.accounts import accounts_bp
        from .backend.accounts.components.accounts_context import accounts_context, inject_now

        app.register_blueprint(landing_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(accounts_bp)

#        from .backend.database.models import MailSettings
#        mail_settings = MailSettings.query.first()
#        if mail_settings.mail_server and mail_settings.company_email and mail_settings.password:
#            app.config['MAIL_SERVER'] = f'smtp.{mail_settings.mail_server}.com'
#            app.config['MAIL_PORT'] = 465
#            app.config['MAIL_USERNAME'] = mail_settings.company_email
#            app.config['MAIL_PASSWORD'] = mail_settings.password
#            app.config['MAIL_USE_TLS'] = False
#            app.config['MAIL_USE_SSL'] = True
#        else:
#            app.config.from_object(MailConfig)
#        mail.init_app(app)

        from .backend.database.models import MailSettings
        app.config.from_object(MailConfig)
        try:
            mail_settings = MailSettings.query.first()
            if mail_settings and mail_settings.mail_server and mail_settings.company_email and mail_settings.password:
                app.config['MAIL_SERVER'] = f'smtp.{mail_settings.mail_server}.com'
                app.config['MAIL_PORT'] = 465
                app.config['MAIL_USERNAME'] = mail_settings.company_email
                app.config['MAIL_PASSWORD'] = mail_settings.password
                app.config['MAIL_USE_TLS'] = False
                app.config['MAIL_USE_SSL'] = True
        except Exception as e:
            print(f"Error fetching mail settings from the database: {e}")
        mail.init_app(app)

        app.context_processor(accounts_context)
        app.context_processor(inject_now)

        from .backend.database.models import User
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        app.jinja_env.globals['csrf_token'] = generate_csrf
        app.jinja_env.filters['format_amount'] = format_amount

    return app
