# app/backend/accounts/dashboard/routes.py
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    # Check if the user is still authenticated
    if current_user.is_authenticated:
        # You can add dashboard-specific logic and data here
        return render_template('accounts/dashboard.html', hide_footer=True)
    else:
        # If the user is not authenticated, redirect to the login page
        return redirect(url_for('auth.login'))
