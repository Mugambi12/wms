# File: app/backend/auth/routes.py

from flask import Blueprint
from flask_login import login_user, login_required
from app.backend.auth.forms import LoginForm, RegistrationForm
from .utils import login_user, register_user, perform_logout


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route for user login.

    Returns:
        redirect/render_template: Redirects to the dashboard if login is successful, else renders the login form.
    """
    form = LoginForm()
    return login_user(form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Route for user registration.

    Returns:
        redirect/render_template: Redirects to login page if registration is successful, else renders registration form.
    """
    form = RegistrationForm()
    return register_user(form)


@auth_bp.route('/register/apogen_admin', methods=['GET', 'POST'])
def register_apogen_admin():
    """
    Route for registering an admin user.

    Returns:
        redirect/render_template: Redirects to login page if registration is successful, else renders registration form.
    """
    form = RegistrationForm()
    return register_user(form, is_admin=True)


@auth_bp.route('/logout')
@login_required
def logout():
    """
    Route for user logout.

    Returns:
        redirect: Redirects to the landing page after successful logout.
    """
    return perform_logout()
