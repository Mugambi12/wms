# File: app/backend/accounts/messages/routes.py

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

messages_bp = Blueprint('messages', __name__, url_prefix='/accounts')

@messages_bp.route('/messages')
@login_required
def messages():
    return render_template('accounts/messages.html', hide_footer=True)
