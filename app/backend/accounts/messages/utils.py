# File: app/backend/accounts/messages/routes.py

from flask_login import current_user
from app import db
from ...database.models import Message, User


def get_unread_message_count(user_id):
    try:
        unread_count = Message.query.filter_by(receiver_id=user_id, is_read=False).count()
        return unread_count
    except Exception as e:
        print(f"Error retrieving unread message count: {e}")
        return None


def get_received_unread_message_count(user_id):
    try:
        unread_count = Message.query.filter(
            (Message.sender_id == user_id) & (Message.receiver_id == current_user.id) & (Message.is_read == False)
        ).count()
        return unread_count
    except Exception as e:
        print(f"Error retrieving unread message count: {e}")
        return None


def get_user_messages(user_id):
    chatting_user = User.query.get(user_id)
    if not chatting_user:
        return [], None

    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp.asc()).all()

    unread_messages = [msg for msg in messages if not msg.is_read and msg.receiver_id == current_user.id]
    for msg in unread_messages:
        msg.is_read = True
        db.session.commit()

    return messages, chatting_user.first_name
