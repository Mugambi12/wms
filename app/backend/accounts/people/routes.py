# app/backend/accounts/people/routes.py
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.backend.models.user import User, db

people_bp = Blueprint('people', __name__, url_prefix='/people')

@people_bp.route('/add_people')
@login_required
def add_people():
    # Check if the user is still authenticated
    if current_user.is_authenticated:
        # You can add people-specific logic and data here
        return render_template('accounts/add_people.html', hide_footer=True)
    else:
        # If the user is not authenticated, redirect to the login page
        return redirect(url_for('auth.login'))

@people_bp.route('/people_list')
@login_required
def people_list():
    # Check if the user is still authenticated
    if current_user.is_authenticated:
        # Query people/user data from the User model
        people_list = User.query.all()  # Adjust the query based on your actual model structure

        # Pass the people_list to the template
        return render_template('accounts/people_list.html', hide_footer=True, people_list=people_list)
    else:
        # If the user is not authenticated, redirect to the login page
        return redirect(url_for('auth.login'))
