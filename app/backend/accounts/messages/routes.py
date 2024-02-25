# File: app/backend/accounts/messages/routes.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from ...database.models import Message, User
from .forms import MessageForm
from .utils import get_received_unread_message_count, send_message, get_user_messages
from .utils import send_broadcast_message, get_broadcast_messages, get_sender_name


messages_bp = Blueprint('messages', __name__, url_prefix='/accounts')


@messages_bp.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    """
    Route for displaying and sending messages.

    This route handles both GET and POST requests. For GET requests, it renders
    the messages template with the message form and user messages. For POST requests,
    it handles the message form submission, sending either a broadcast message to all
    users or a message to a specific user.

    Returns:
        render_template: Renders the messages template with appropriate context variables.
        redirect: Redirects to the messages route after form submission.
    """
    form = MessageForm()

    if request.method == 'POST' and form.validate_on_submit():
        if form.receiver_id.data == 0:
            # Broadcast message to all users
            if send_broadcast_message(current_user.id, form.content.data):
                flash('Broadcast message sent successfully!', 'success')
            else:
                flash('Failed to send broadcast message.', 'error')
        else:
            # Send message to a specific user
            receiver_id = form.receiver_id.data
            content = form.content.data

            if send_message(current_user.id, receiver_id, content):
                flash('Message sent successfully!', 'success')
            else:
                flash('Failed to send message.', 'error')

        return redirect(url_for('accounts.messages.messages'))


    # Fetch all users and their unread message counts
    all_users = User.query.all()
    unread_sent_message_counts = {user.id: get_received_unread_message_count(user.id) for user in all_users}

    selected_user_id = request.args.get('user_id')
    messages = []
    chatting_user_first_name = None
    if selected_user_id == '0':
        # Retrieve broadcast messages
        chatting_user_first_name = "Broadcast Message"
        messages = get_broadcast_messages()
    else:
        # Retrieve messages for a specific user
        messages, chatting_user_first_name = get_user_messages(selected_user_id)

    all_messages = Message.query.all()

    return render_template('accounts/messages.html',
                            form=form,
                            messages=messages,
                            all_users=all_users,
                            unread_sent_message_counts=unread_sent_message_counts,
                            hide_footer=True,
                            chatting_user_first_name=chatting_user_first_name,
                            all_messages=all_messages,
                            get_sender_name=get_sender_name)
