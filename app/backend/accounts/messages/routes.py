# File: app/backend/accounts/messages/routes.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from ...database.models import Message, User
from .forms import MessageForm


messages_bp = Blueprint('messages', __name__, url_prefix='/accounts')


def get_unread_message_count(user_id):
    try:
        unread_count = Message.query.filter_by(receiver_id=user_id, is_read=False).count()
        return unread_count
    except Exception as e:
        print(f"Error retrieving unread message count: {e}")
        return None

def get_received_unread_message_count(user_id):
    try:
        unread_count = Message.query.filter_by(sender_id=user_id, is_read=False).count()
        return unread_count
    except Exception as e:
        print(f"Error retrieving unread message count: {e}")
        return None



def get_user_messages(user_id):
    chatting_user = User.query.get(user_id)  # Fetch user object for the other user
    if not chatting_user:
        return [], None  # Return an empty list if user not found

    # Fetch messages exchanged between current user and the other user
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp.asc()).all()

    # Mark unread messages as read
    unread_messages = [msg for msg in messages if not msg.is_read and msg.receiver_id == current_user.id]
    for msg in unread_messages:
        msg.is_read = True
        db.session.commit()

    return messages, chatting_user.first_name

@messages_bp.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
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
