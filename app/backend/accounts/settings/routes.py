# app/backend/accounts/settings/routes.py
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

@settings_bp.route('/settings')
@login_required
def settings():
    # Check if the user is still authenticated
    if current_user.is_authenticated:
        # You can add settings-specific logic and data here
        return render_template('accounts/settings.html', hide_footer=True)
    else:
        # If the user is not authenticated, redirect to the login page
        return redirect(url_for('auth.login'))
