# File: app/backend/auth/routes.py

from datetime import datetime, timezone, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash, make_response, request
from flask_login import login_user, login_required, logout_user, current_user
from app.backend.database.models import User, db
from app.backend.auth.forms import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        mobile_number_last_9 = form.mobile_number.data.strip()[-9:]

        user = User.query.filter_by(mobile_number=mobile_number_last_9).first()

        if user and user.check_password(form.password.data):
            if user.is_active:
                # Update last login time
                user.last_login = datetime.now(timezone.utc) + timedelta(hours=3)
                db.session.commit()

                login_user(user)
                flash(f'Welcome back, {user.first_name.title()}! You have successfully logged in.', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('accounts.dashboard.dashboard'))
            else:
                flash('Your account is inactive. Please contact support for assistance.', 'warning')
        else:
            flash('Invalid mobile number or password. Please check and try again.', 'danger')

    return render_template('auth/login.html', form=form, hide_navbar=True, hide_sidebar=True, hide_footer=True)


@auth_bp.route('/register/apogen_admin', methods=['GET', 'POST'])
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the user already exists
        existing_user = User.query.filter_by(mobile_number=form.mobile_number.data[-9:]).first()
        if existing_user:
            flash('User already exists. Please log in instead.', 'info')
            return redirect(url_for('auth.login'))

        # Create a new user
        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            mobile_number=form.mobile_number.data[-9:],
            password=form.password.data
        )

        # Check if it's the admin registration route
        if 'apogen_admin' in request.url_rule.rule:
            new_user.is_admin = True

        new_user.unique_user_id = new_user.generate_unique_user_id()

        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    else:
        if request.method == 'POST':
            if 'mobile_number' in form.errors:
                flash('Invalid mobile number. Please enter a valid mobile number.', 'danger')
            if 'password' or 'confirm_password' in form.errors:
                flash('Passwords do not match. Please re-enter your password.', 'danger')

    return render_template('auth/register.html', form=form, hide_navbar=True, hide_sidebar=True, hide_footer=True)



@auth_bp.route('/logout')
@login_required
def logout():
    user_name = current_user.first_name.title()

    # Update last logout time
    current_user.last_logout = datetime.now(timezone.utc) + timedelta(hours=3)
    db.session.commit()

    logout_user()
    flash(f'Goodbye, {user_name}! You have been successfully logged out.', 'info')

    response = make_response(redirect(url_for('landing.landing')))

    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response
