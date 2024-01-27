from flask import Blueprint, render_template

messages_bp = Blueprint('messages', __name__, url_prefix='/accounts')

@messages_bp.route('/messages')
def messages():
    # You can add messages-specific logic and data here
    return render_template('accounts/messages.html', hide_footer=True)
