# File: app/backend/accounts/messages/utils.py

from flask_login import current_user
from core import db
from ...database.models import Message, User


def get_unread_message_count_for_navbar(user_id):
    """
    Retrieve the count of unread messages for a given user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        int or None: The count of unread messages, or None if an error occurs.
    """
    try:
        unread_count = Message.query.filter_by(receiver_id=user_id, is_read=False).count()
        return unread_count
    except Exception as e:
        print(f"Error retrieving unread message count for user {user_id}: {e}")
        return None


def send_message(sender_id, receiver_id, content):
    """
    Send a message to a specific user.

    Args:
        sender_id (int): The ID of the sender.
        receiver_id (int): The ID of the receiver.
        content (str): The content of the message.

    Returns:
        bool: True if the message was sent successfully, False otherwise.
    """
    try:
        new_message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
        db.session.add(new_message)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error sending message: {e}")
        db.session.rollback()
        return False


def get_user_messages(user_id):
    """
    Retrieve messages exchanged between the current user and another user.

    Args:
        user_id (int): The ID of the other user.

    Returns:
        tuple: A tuple containing a list of messages and the first name of the other user.
    """
    if user_id is None:
        return [], None

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

    return messages, chatting_user.id


def get_received_unread_message_count(user_id):
    """
    Retrieve the count of unread messages received by the current user from a specific user.

    Args:
        user_id (int): The ID of the user whose messages are being checked.

    Returns:
        int or None: The count of unread messages, or None if an error occurs.
    """
    try:
        unread_count = Message.query.filter(
            (Message.sender_id == user_id) & (Message.receiver_id == current_user.id) & (Message.is_read == False)
        ).count()
        return unread_count
    except Exception as e:
        print(f"Error retrieving unread message count for user {user_id}: {e}")
        return None


def send_broadcast_message(sender_id, content):
    """
    Send a broadcast message to all users.

    Args:
        sender_id (int): The ID of the sender.
        content (str): The content of the message.

    Returns:
        bool: True if the broadcast message was sent successfully, False otherwise.
    """
    try:
        all_users = User.query.all()
        for user in all_users:
            new_message = Message(sender_id=sender_id, receiver_id=user.id, content=content)
            db.session.add(new_message)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error sending broadcast message: {e}")
        db.session.rollback()
        return False


def get_broadcast_messages():
    """
    Retrieve broadcast messages sent to all users.

    Returns:
        list: A list of broadcast messages.
    """
    try:
        broadcast_messages = Message.query.filter(Message.receiver_id == '0').order_by(Message.timestamp.asc()).all()
        return broadcast_messages
    except Exception as e:
        print(f"Error retrieving broadcast messages: {e}")
        return []


def get_sender_name(sender_id):
    """
    Retrieve the first name of the user who sent the message.

    Args:
        sender_id (int): The ID of the sender.

    Returns:
        str: The first name of the sender.
    """
    sender = User.query.get(sender_id)
    return sender.first_name.title() if sender else "Unknown"
