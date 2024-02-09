# app/backend/accounts/dashboard/routes.py
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    # You can add dashboard-specific logic and data here
    return render_template('accounts/dashboard.html', hide_footer=True)
