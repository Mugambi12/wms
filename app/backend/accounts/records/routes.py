# app/backend/accounts/records/routes.py
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

records_bp = Blueprint('records', __name__, url_prefix='/records')

@records_bp.route('/meter_readings')
@login_required
def meter_readings():
    # Check if the user is still authenticated
    if current_user.is_authenticated:
        # You can add records-specific logic and data here
        return render_template('accounts/meter_readings.html', hide_footer=True)
    else:
        # If the user is not authenticated, redirect to the login page
        return redirect(url_for('auth.login'))

@records_bp.route('/billing')
@login_required
def billing():
    # Check if the user is still authenticated
    if current_user.is_authenticated:
        # You can add records-specific logic and data here
        return render_template('accounts/billing.html', hide_footer=True)
    else:
        # If the user is not authenticated, redirect to the login page
        return redirect(url_for('auth.login'))

@records_bp.route('/payments')
@login_required
def payments():
    # Check if the user is still authenticated
    if current_user.is_authenticated:
        # You can add records-specific logic and data here
        return render_template('accounts/payments.html', hide_footer=True)
    else:
        # If the user is not authenticated, redirect to the login page
        return redirect(url_for('auth.login'))
