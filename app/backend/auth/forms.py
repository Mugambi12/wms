# app/backend/auth/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.backend.database.models import User

class LoginForm(FlaskForm):
    mobile_number = StringField('Mobile Number', validators=[DataRequired(), Length(min=9, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Length(max=50)])
    mobile_number = StringField('Mobile Number', validators=[DataRequired(), Length(min=9, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_mobile_number(self, field):
        mobile_number = field.data.strip()[-9:]
        if User.query.filter_by(mobile_number=mobile_number).first():
            raise ValidationError('Mobile number is already registered.')
