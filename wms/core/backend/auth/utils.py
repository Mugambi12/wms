from flask import render_template, redirect, url_for, flash, make_response, request
from flask_login import login_user, logout_user, current_user
from core import db
from ..database.models import *


def _login_user(form):
    """
    Internal function for handling user login.

    Args:
        form (LoginForm): Form containing user login data.

    Returns:
        redirect/render_template: Redirects to the dashboard if login is successful, else renders the login form.
    """
    if form.validate_on_submit():
        mobile_number_last_9 = form.mobile_number.data.strip()[-9:]

        user = User.query.filter_by(mobile_number=mobile_number_last_9).first()

        if user and user.check_password(form.password.data):
            if user.is_active:
                user.last_login = default_datetime()
                db.session.commit()

                login_user(user)
                if current_user.last_logout is None:
                    flash(f'Welcome, {user.first_name.title()}! Glad you have joined us.', 'success')
                else:
                    flash(f'Welcome back, {user.first_name.title()}! Glad to see you back.', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('accounts.dashboard.dashboard'))
            else:
                flash('Your account is inactive. Please contact support for assistance.', 'warning')
        else:
            flash('Invalid mobile number or password. Please check and try again.', 'danger')

    return render_template('auth/login.html',
                           form=form,
                           title="Login",
                           hide_navbar=True,
                           hide_sidebar=True,
                           hide_footer=True)


def _register_user(form, is_admin=False):
    """
    Internal function for registering a user.

    Args:
        form (RegistrationForm): Form containing user data.
        is_admin (bool, optional): Indicates if the user is an admin. Defaults to False.

    Returns:
        redirect/render_template: Redirects to login page if registration is successful, else renders registration form.
    """
    if form.validate_on_submit():
        mobile_number_last_9 = form.mobile_number.data.strip()[-9:]
        existing_user = User.query.filter_by(mobile_number=mobile_number_last_9).first()

        if existing_user:
            flash('User already exists. Please log in instead.', 'info')
            return redirect(url_for('auth.login'))

        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            mobile_number=form.mobile_number.data[-9:],
            password=form.password.data
        )

        if is_admin:
            new_user.is_admin = True
        else:
            new_user.is_active = False

        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    elif request.method == 'POST':
        error_messages = {
            'mobile_number': 'Invalid mobile number. Please enter a valid mobile number.',
            'email': 'Invalid email address. Please enter a valid email.',
            'password': 'Passwords do not match. Please re-enter your password.'
        }
        for field, message in error_messages.items():
            if field in form.errors:
                flash(message, 'danger')

    return render_template('auth/register.html',
                           form=form,
                           title="Register",
                           hide_navbar=True,
                           hide_sidebar=True,
                           hide_footer=True)


def perform_logout():
    """
    Performs the logout process for the current user.

    Returns:
        redirect: Redirects to the landing page after successful logout.
    """
    user_name = current_user.first_name.title()
    current_user.last_logout = default_datetime()
    db.session.commit()
    logout_user()
    flash(f'Goodbye, {user_name}! You have been successfully logged out.', 'info')

    response = make_response(redirect(url_for('landing.landing')))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response
