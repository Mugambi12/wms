# app/backend/accounts/people/routes.py

import os
from flask import flash, url_for, current_app
from flask_login import current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from core import db
from ...database.models import User


def handle_add_new_users(form, current_user):
    """
    Handles the addition of new users.

    Args:
        form: The form containing user data.
        current_user: The current user performing the action.

    Returns:
        dict: A dictionary indicating the success status and a message.
    """
    mobile_number = form.mobile_number.data[-9:]
    first_name = form.first_name.data
    last_name = form.last_name.data
    email = form.email.data
    house_section = form.house_section.data
    house_number = form.house_number.data
    password = form.password.data
    confirm_password = form.confirm_password.data

    if not all([mobile_number, first_name, last_name, email, house_section, house_number, password]):
        messages = []
        if not mobile_number:
            messages.append('Mobile number is required.')
        if not first_name:
            messages.append('First name is required.')
        if not last_name:
            messages.append('Last name is required.')
        if not email:
            messages.append('Email is required.')
        if not house_section:
            messages.append('House section is required.')
        if not house_number:
            messages.append('House number is required.')
        if not password:
            messages.append('Password is required.')
        return {'success': False, 'message': ', '.join(messages)}

    if password != confirm_password:
        return {'success': False, 'message': 'Passwords do not match. Please make sure your passwords match.'}

    try:
        existing_user = User.query.filter_by(mobile_number=mobile_number).first()
        if existing_user:
            return {'success': False, 'message': 'Mobile number is already registered.'}

        existing_house = User.query.filter_by(house_section=house_section, house_number=house_number).first()
        if existing_house:
            return {'success': False, 'message': 'Household is already registered.'}

        new_user = User(
            mobile_number=mobile_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            house_section=house_section,
            house_number=house_number,
            password=password
        )
        db.session.add(new_user)
        db.session.commit()

        return {'success': True, 'message': f'{first_name.title()} has been successfully added as a user.'}

    except Exception as e:
        return {'success': False, 'message': f'Error adding user: {str(e)}'}


def change_password(user, form):
    """
    Handles changing the password for a user.

    Args:
        user: The user whose password is being changed.
        form: The form containing password data.

    Returns:
        bool: True if the password change was successful, False otherwise.
    """
    if current_user.is_admin and form.current_password.data:
        if not user.check_password(form.current_password.data):
            flash('Current password is incorrect.', 'danger')
            return False

        if form.new_password.data:
            user.password_hash = generate_password_hash(form.new_password.data)

    return True


def validate_new_password(password):
    """
    Validates a new password.

    Args:
        password (str): The password to validate.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    return len(password) >= 6


def save_profile_picture(profile_picture):
    """
    Saves a user's profile picture.

    Args:
        profile_picture: The profile picture to save.

    Returns:
        bool: True if the profile picture was saved successfully, False otherwise.
    """
    try:
        filename = secure_filename(f"{current_user.mobile_number}.png")

        uploads_folder = os.path.join(current_app.root_path, 'frontend', 'static', 'uploads', 'profile')
        save_path = os.path.join(uploads_folder, filename)

        profile_picture.save(save_path)
        current_user.profile_image = url_for('static', filename=f'uploads/profile/{filename}')
        db.session.commit()
        return True
    except Exception as e:
        print(f'Error saving profile picture: {str(e)}')
        return False


def delete_user(user):
    """
    Deletes a user from the database.

    Args:
        user: The user to be deleted.

    Returns:
        bool: True if the user was deleted successfully, False otherwise.
    """
    try:
        db.session.delete(user)
        db.session.commit()
        return True
    except Exception as e:
        print(f'Error deleting user: {str(e)}')
        return False
