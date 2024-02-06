# app/backend/accounts/people/routes.py
import os
from flask import flash,  url_for, current_app
from flask_login import current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from app import db
from ...models.user import User


def handle_add_new_users(form):
    mobile_number = form.mobile_number.data
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
            return {'success': False, 'message': 'Failed to add user. Mobile number is already registered.'}

        # Check if the household is already registered
        existing_household = User.query.filter_by(house_section=house_section, house_number=house_number).first()
        if existing_household:
            return {'success': False, 'message': 'Failed to add user. Household is already registered.'}

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

        db.session.add(new_user)
        db.session.commit()

        return {'success': True, 'message': f'{first_name.title()} has been successfully added as a user.'}

    except Exception as e:
        return {'success': False, 'message': f'Failed to add user. An error occurred: {str(e)}'}

def handle_edit_user(user, form):
    if form.new_password.data:
        if not validate_new_password(form.new_password.data):
            return {'success': False, 'message': 'New password must be at least 6 characters long.', 'alert': 'danger'}

    if change_password(user, form):
        form.populate_obj(user)
        db.session.commit()
        return {'success': True, 'message': f'Successfully updated profile for {user.first_name.title()}.', 'alert': 'success'}
    else:
        return {'success': False, 'message': 'Error updating profile.', 'alert': 'danger'}

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

def handle_edit_profile_picture(form, current_user):
    if form.profile_image.data:
        profile_picture = form.profile_image.data

        filename = secure_filename(f"{current_user.mobile_number}.png")

        uploads_folder = os.path.join(current_app.root_path, 'assets', 'static', 'uploads', 'profile')
        save_path = os.path.join(uploads_folder, filename)

        try:
            profile_picture.save(save_path)
            current_user.profile_image = url_for('static', filename=f'uploads/profile/{filename}')
            db.session.commit()
            return {'message': 'Profile picture updated successfully.', 'alert': 'success'}
        except Exception as e:
            return {'message': f'Error updating profile picture: {str(e)}', 'alert': 'danger'}
    else:
        return {'message': 'No profile picture provided.', 'alert': 'danger'}

def handle_delete_user(user_id):
    user = User.query.get_or_404(user_id)

    if user == current_user:
        return {'message': 'You cannot delete your own account.', 'alert': 'danger'}

    db.session.delete(user)
    db.session.commit()
    return {'message': f'Successfully deleted the user {user.first_name.title()}.', 'alert': 'success'}
