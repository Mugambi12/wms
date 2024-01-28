# app/backend/accounts/messages/routes.py
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

messages_bp = Blueprint('messages', __name__, url_prefix='/accounts')

@messages_bp.route('/messages')
@login_required
def messages():
    # Check if the user is still authenticated
    if current_user.is_authenticated:
        # You can add messages-specific logic and data here
        return render_template('accounts/messages.html', hide_footer=True)
    else:
        # If the user is not authenticated, redirect to the login page
        return redirect(url_for('auth.login'))
