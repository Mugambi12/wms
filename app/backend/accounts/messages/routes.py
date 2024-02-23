# File: app/backend/accounts/messages/routes.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from ...database.models import Message, User
from .forms import MessageForm
from .utils import get_received_unread_message_count, get_unread_message_count, get_user_messages

messages_bp = Blueprint('messages', __name__, url_prefix='/accounts')

@messages_bp.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    """
    Route for displaying and sending messages.

    GET: Renders the message template with message form and user messages.
    POST: Handles message form submission and sends the message.

    Returns:
        render_template: Renders the messages template.
        redirect: Redirects to the messages route.
    """
    form = MessageForm()

    if request.method == 'POST' and form.validate_on_submit():
        receiver_id = form.receiver_id.data
        content = form.content.data

        new_message = Message(sender_id=current_user.id, receiver_id=receiver_id, content=content)
        db.session.add(new_message)
        db.session.commit()
        flash('Message sent successfully!', 'success')
        return redirect(url_for('accounts.messages.messages', user_id=receiver_id))

    # Fetch all users and their unread message counts
    all_users = User.query.all()
    unread_message_counts = {user.id: get_unread_message_count(user.id) for user in all_users}
    unread_sent_message_counts = {user.id: get_received_unread_message_count(user.id) for user in all_users}

    selected_user_id = request.args.get('user_id')
    messages = []
    chatting_user_first_name = None
    if selected_user_id:
        messages, chatting_user_first_name = get_user_messages(selected_user_id)

    all_messages = Message.query.all()

    return render_template('accounts/messages.html',
                            form=form,
                            messages=messages,
                            all_users=all_users,
                            unread_message_counts=unread_message_counts,
                            unread_sent_message_counts=unread_sent_message_counts,
                            hide_footer=True,
                            chatting_user_first_name=chatting_user_first_name,
                            all_messages=all_messages)
