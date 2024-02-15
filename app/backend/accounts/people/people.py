# app/backend/accounts/people/routes.py
import os
from flask import flash,  url_for, current_app
from flask_login import current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from app import db
from ...models.user import User

def handle_add_new_users(form, current_user):
    mobile_number = form.mobile_number.data[-9:]
    first_name = form.first_name.data
    last_name = form.last_name.data
    email = form.email.data
    house_section = form.house_section.data
    house_number = form.house_number.data
    password = form.password.data

    try:
        # Check if the mobile number is already registered
        existing_user = User.query.filter_by(mobile_number=mobile_number).first()
        if existing_user:
            return {'success': False, 'message': 'Mobile number is already registered.'}
        existing_house = User.query.filter_by(house_section=house_section, house_number=house_number).first()
        if existing_house:
            return {'success': False, 'message': 'Household is already registered.'}

        # Create a new user object
        new_user = User(
            mobile_number=mobile_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            house_section=house_section,
            house_number=house_number,
            password=password
        )

        new_user.unique_user_id = new_user.generate_unique_user_id()

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return {'success': True, 'message': f'{first_name.title()} has been successfully added as a user.'}

    except Exception as e:
        # Handle any errors that occur during user creation
        return {'success': False, 'message': f'Error adding user: {str(e)}'}

def change_password(user, form):
    if current_user.is_admin and form.current_password.data:
        if not user.check_password(form.current_password.data):
            flash('Current password is incorrect.', 'danger')
            return False

        if form.new_password.data:
            user.password_hash = generate_password_hash(form.new_password.data)

    return True

def validate_new_password(password):
    return len(password) >= 6

def save_profile_picture(profile_picture):
    try:
        filename = secure_filename(f"{current_user.mobile_number}.png")

        uploads_folder = os.path.join(current_app.root_path, 'assets', 'static', 'uploads', 'profile')
        save_path = os.path.join(uploads_folder, filename)

        profile_picture.save(save_path)
        current_user.profile_image = url_for('static', filename=f'uploads/profile/{filename}')
        db.session.commit()
        return True
    except Exception as e:
        print(f'Error saving profile picture: {str(e)}')
        return False

def delete_user(user):
    try:
        db.session.delete(user)
        db.session.commit()
        return True
    except Exception as e:
        print(f'Error deleting user: {str(e)}')
        return False
