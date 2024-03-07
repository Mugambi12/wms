# File: app/backend/auth/routes.py

from flask import Blueprint
from flask_login import login_required
from app.backend.auth.forms import LoginForm, RegistrationForm
from .utils import _login_user, _register_user, perform_logout


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route for user login.

    Returns:
        redirect/render_template: Redirects to the dashboard if login is successful, else renders the login form.
    """
    form = LoginForm()
    return _login_user(form)


@auth_bp.route('/logout')
@login_required
def logout():
    """
    Route for user logout.

    Returns:
        redirect: Redirects to the landing page after successful logout.
    """
    return perform_logout()


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Route for user registration.

    Returns:
        redirect/render_template: Redirects to login page if registration is successful, else renders registration form.
    """
    form = RegistrationForm()
    return _register_user(form)


@auth_bp.route('/register/apogen_admin', methods=['GET', 'POST'])
def register_apogen_admin():
    """
    Route for registering an admin user.

    Returns:
        redirect/render_template: Redirects to login page if registration is successful, else renders registration form.
    """
    form = RegistrationForm()
    return _register_user(form, is_admin=True)





# Update forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    token = HiddenField()  # Add a hidden field for the token
    submit = SubmitField('Reset Password')


import secrets
import string
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from flask import current_app, url_for
from app import mail

def generate_random_string(length=32):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    salt = current_app.config.get('SECURITY_PASSWORD_SALT', generate_random_string())
    return serializer.dumps(email, salt=salt)

def send_password_reset_email(email, token):
    reset_link = url_for('auth.reset_password', token=token, _external=True)
    sender_email = current_app.config['MAIL_USERNAME']
    msg = Message('Password Reset Request', recipients=[email], sender=sender_email)
    msg.body = f'To reset your password, click on the following link: {reset_link}'
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


# Update routes.py
from flask import flash, redirect, url_for, render_template
from ..database.models import User, PasswordResetToken, db

@auth_bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    form = PasswordResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            token = generate_token(form.email.data)
            reset_token = PasswordResetToken(email=form.email.data, token=token)
            db.session.add(reset_token)
            db.session.commit()
            if send_password_reset_email(form.email.data, token):
                flash('An email with instructions to reset your password has been sent.', 'info')
            else:
                flash('Failed to send password reset email. Please try again later.', 'danger')
        else:
            flash('Email not found in our users.', 'warning')

        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password_request.html', form=form, hide_navbar=True, hide_sidebar=True, hide_footer=True)

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    reset_token = PasswordResetToken.query.filter_by(token=token).first_or_404()
    form = ResetPasswordForm()

    if form.validate_on_submit():
        # Find the user by email
        user = User.query.filter_by(email=reset_token.email).first()

        if user:
            # Update user password
            user.password = form.password.data
            # Delete the reset token
            db.session.delete(reset_token)
            db.session.commit()
            flash('Your password has been reset successfully.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid user or expired token.', 'danger')
            return redirect(url_for('auth.reset_password_request'))

    # Pass the token to the template
    form.token.data = token
    return render_template('auth/reset_password.html', form=form, token=token, hide_navbar=True, hide_sidebar=True, hide_footer=True), 204








#@auth_bp.route('/send_mail_to_user', methods=['GET', 'POST'])
#def send_mail_to_user():
#    form = PasswordResetForm()
#
#    if form.validate_on_submit():
#        msg = Message("Hey", sender='noreply@apogen.com', recipients=[form.email.data])
#        msg.body = "Hey how are you doing today. This is Apogen Software Solutions"
#
#        mail.send(msg)
#        return "Message sent successfully"
#
#    return render_template('auth/send_mail_to_user.html', form=form, hide_navbar=True, hide_sidebar=True, hide_footer=True)
