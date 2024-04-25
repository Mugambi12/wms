from flask import flash, redirect, url_for, render_template, current_app, jsonify
from werkzeug.security import generate_password_hash
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

from core import mail, db
from core.utils import generate_random_string
from ..database.models import User, PasswordResetToken


def generate_token(email):
    with current_app.app_context():
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        salt = current_app.config.get('SECURITY_PASSWORD_SALT', generate_random_string())
        return serializer.dumps(email, salt=salt)


def send_async_email(msg):
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def send_password_reset_email(email, token):
    reset_link = url_for('auth.reset_password', token=token, _external=True)

    sender_email = current_app.config['MAIL_USERNAME']

    msg = Message('Password Reset Request', recipients=[email], sender=sender_email)

    user = User.query.filter_by(email=email).first()
    user_name = f"{user.first_name} {user.last_name}"

    email_body = (
        "<html>"
        "<head>"
        "<style>"
        ".card {"
        "   background-color: #f9f9f9;"
        "   border-radius: 10px;"
        "   box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);"
        "   padding: 25px;"
        "   max-width: 600px;"
        "   margin: auto;"
        "   text-align: center;"
        "}"
        ".header {"
        "   font-size: 28px;"
        "   font-weight: bold;"
        "   margin-bottom: 20px;"
        "   color: #333333;"
        "}"
        ".content {"
        "   font-size: 18px;"
        "   margin-bottom: 15px;"
        "   color: #666666;"
        "}"
        ".button {"
        "   background-color: #007bff;"
        "   color: #ffffff;"
        "   padding: 12px 24px;"
        "   text-decoration: none;"
        "   border-radius: 5px;"
        "   display: inline-block;"
        "   font-size: 18px;"
        "   margin-top: 30px;"
        "}"
        ".signature {"
        "   color: #666666;"
        "   font-size: 14px;"
        "}"
        "</style>"
        "</head>"
        "<body style='background-color: #f5f5f5;'>"
        "<div class='card'>"
        f"<p class='header'>Dear <span style='color: #007bff;'>{user_name.title()}</span>,</p>"
        "<p class='content'>We've received a request to reset your password. If this wasn't you, no action is required.</p>"
        "<p class='content'>To reset your password, please click the button below:</p>"
        f"<a href=\"{reset_link}\" class=\"button\" style='color: #ffffff;'>Reset Password</a>"
        "<p class='content'>If you're unable to click the button, you can copy and paste the following link into your browser's address bar:</p>"
        f"<p class='content'>{reset_link}</p>"
        "<p class='content'>This link will expire after a certain period of time for security reasons.</p>"
        "<p class='content'>If you have any questions or need further assistance, please don't hesitate to contact us.</p>"
        "<p class='signature'>Best regards,<br>ApoGen Sonic Team</p>"
        "</div>"
        "</body>"
        "</html>"
    )

    msg.body = email_body
    msg.html = email_body

    return send_async_email(msg)


def _reset_password_request(form):
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            token = generate_token(form.email.data)
            reset_token = PasswordResetToken(email=form.email.data, token=token)
            db.session.add(reset_token)
            db.session.commit()
            if send_password_reset_email(form.email.data, token):
                return jsonify({"message": "An email with instructions to reset your password has been sent.", "type": "success"})
            else:
                return jsonify({"message": "Failed to send password reset email. Please try again later.", "type": "danger"})
        else:
            return jsonify({"message": "Email not found in our users.", "type": "warning"})

    return render_template(
        'auth/reset_password_request.html',
        form=form,
        title="Reset Password",
        hide_navbar=True,
        hide_sidebar=True,
        hide_footer=True
    )


def _reset_password(form, token):
    reset_token = PasswordResetToken.query.filter_by(token=token).first_or_404()

    if form.validate_on_submit():
        user = User.query.filter_by(email=reset_token.email).first()

        if user:
            user.password_hash = generate_password_hash(form.password.data)

            db.session.delete(reset_token)
            db.session.commit()

            flash('Your password has been reset successfully.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid user or expired token.', 'danger')
            return redirect(url_for('auth.reset_password_request'))

    form.token.data = token
    return render_template(
        'auth/reset_password.html',
        form=form,
        token=token,
        hide_navbar=True,
        hide_sidebar=True,
        hide_footer=True
    )
