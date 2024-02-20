# File: app/backend/accounts/messages/routes.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from ...database.models import Message, User
from .forms import MessageForm

from flask import jsonify


messages_bp = Blueprint('messages', __name__, url_prefix='/accounts')

def get_unread_message_count(user_id):
    try:
        # Query the database for unread messages for the given user
        unread_count = Message.query.filter_by(receiver_id=user_id, is_read=False).count()
        return unread_count
    except Exception as e:
        # Handle any exceptions, such as database connection errors
        print(f"Error retrieving unread message count: {e}")
        return None

@messages_bp.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    if request.method == 'POST':
        # Process message sending
        form = MessageForm()
        if form.validate_on_submit():
            receiver_id = form.receiver_id.data
            content = form.content.data

            # Create a new message instance
            new_message = Message(sender_id=current_user.id, receiver_id=receiver_id, content=content)
            db.session.add(new_message)
            db.session.commit()
            flash('Message sent successfully!', 'success')
            return redirect(url_for('accounts.messages.messages'))

        else:
            flash('Invalid form submission for sending the message.', 'danger')

    # Fetch messages where the current user is either the sender or receiver
    user_id = current_user.id
    messages = Message.query.filter((Message.sender_id == user_id) | (Message.receiver_id == user_id)).all()

    # Fetch all users
    all_users = User.query.all()

    # Initialize unread message count dictionary
    unread_message_counts = {}

    # Calculate unread message count for each user
    for user in all_users:
        unread_count = get_unread_message_count(user.id)
        unread_message_counts[user.id] = unread_count

    # Fetch conversation messages if a user is selected
    selected_user_id = request.args.get('user_id')
    if selected_user_id:
        messages = Message.query.filter(
            ((Message.sender_id == current_user.id) & (Message.receiver_id == selected_user_id)) |
            ((Message.sender_id == selected_user_id) & (Message.receiver_id == current_user.id))
        ).order_by(Message.timestamp.asc()).all()

        # Mark messages as read
        unread_messages = [msg for msg in messages if not msg.is_read and msg.receiver_id == current_user.id]
        for msg in unread_messages:
            msg.is_read = True
            db.session.commit()

    # Fetch all users
    all_messages = Message.query.all()

    return render_template('accounts/messages.html',
                            messages=messages,
                            all_users=all_users,
                           unread_message_counts=unread_message_counts,
                           hide_footer=True,

                           all_messages=all_messages)
