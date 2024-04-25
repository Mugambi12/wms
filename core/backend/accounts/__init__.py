from flask import Blueprint

from .messages.routes import messages_bp
from .dashboard.routes import dashboard_bp
from .people.routes import people_bp
from .records.routes import records_bp
from .expenses.routes import expenses_bp
from .website.routes import website_bp
from .settings.routes import settings_bp
from .components.accounts_context import accounts_context

accounts_bp = Blueprint('accounts', __name__, url_prefix='/accounts')

accounts_bp.register_blueprint(messages_bp)
accounts_bp.register_blueprint(dashboard_bp)
accounts_bp.register_blueprint(people_bp)
accounts_bp.register_blueprint(records_bp)
accounts_bp.register_blueprint(expenses_bp)
accounts_bp.register_blueprint(website_bp)
accounts_bp.register_blueprint(settings_bp)
accounts_bp.context_processor(accounts_context)
