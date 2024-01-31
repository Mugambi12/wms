# app/backend/accounts/security/routes.py
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

security_bp = Blueprint('security', __name__, url_prefix='/security')

@security_bp.route('/security_options')
@login_required
def security_options():
    # Check if the user is still authenticated
    if current_user.is_authenticated:
        # You can add security-specific logic and data here
        return render_template('accounts/security_options.html', hide_footer=True)
    else:
        # If the user is not authenticated, redirect to the login page
        return redirect(url_for('auth.login'))

