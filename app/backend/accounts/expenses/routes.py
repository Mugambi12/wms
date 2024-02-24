# File: app/backend/accounts/security/routes.py

from flask import Blueprint, render_template
from flask_login import login_required


expenses_bp = Blueprint('expenses', __name__, url_prefix='/expenses')


@expenses_bp.route('/expenses')
@login_required
def expenses():
    return render_template('accounts/expenses.html', hide_footer=True)
