# File: app/backend/accounts/messages/routes.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from core import db
from ...database.models import Message, User
from .forms import MessageForm
from .utils import *


messages_bp = Blueprint('messages', __name__, url_prefix='/accounts')


@messages_bp.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    form = MessageForm()

    if request.method == 'POST' and form.validate_on_submit():
        if form.receiver_id.data == 0:
            if not send_broadcast_message(current_user.id, form.content.data):
                flash('Failed to send broadcast message.', 'error')
        else:
            receiver_id = form.receiver_id.data
            content = form.content.data

            if not send_message(current_user.id, receiver_id, content):
                flash('Failed to send message.', 'error')

        return redirect(url_for('accounts.messages.messages', user_id=receiver_id))

    all_users = User.query.all() if current_user.is_admin else User.query.filter(User.is_admin).all()
    unread_sent_message_counts = {user.id: get_received_unread_message_count(user.id) for user in all_users}

    selected_user_id = request.args.get('user_id')
    messages = []
    chatting_user_id = None
    if selected_user_id == '0':
        chatting_user_id = '0'
        messages = get_broadcast_messages()
    else:
        messages, chatting_user_id = get_user_messages(selected_user_id)

    return render_template('accounts/messages.html',
                            form=form,
                            messages=messages,
                            all_users=all_users,
                            unread_sent_message_counts=unread_sent_message_counts,
                            hide_footer=True,
                            chatting_user_id=chatting_user_id,
                            get_sender_name=get_sender_name,
                           title="Messaging")
