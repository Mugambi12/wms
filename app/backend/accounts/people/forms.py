# app/backend/accounts/people/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import EqualTo, DataRequired, Email, Length, Optional, ValidationError
from flask_wtf.file import FileField, FileAllowed
from app.backend.models.user import User


class AddUserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    mobile_number = StringField('Mobile Number', validators=[DataRequired(), Length(min=10, max=20)])
    email = StringField('Email', validators=[DataRequired(), Length(max=50)])
    house_section = StringField('House Section', validators=[DataRequired(), Length(max=50)])
    house_number = StringField('House Number', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_mobile_number(self, field):
        if User.query.filter_by(mobile_number=field.data).first():
            raise ValidationError('Mobile number is already registered.')

class EditUserForm(FlaskForm):
    first_name = StringField('First Name', validators=[Optional()])
    last_name = StringField('Last Name', validators=[Optional()])
    mobile_number = StringField('Mobile Number', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(), Optional()])
    house_section = StringField('House Section', validators=[Optional()])
    house_number = StringField('House Number', validators=[Optional()])
    profile_image = StringField('Profile Image URL', validators=[Optional()])
    is_active = BooleanField('Active', validators=[Optional()])
    is_admin = BooleanField('Admin', validators=[Optional()])
    current_password = PasswordField('Current Password', validators=[Optional()])
    new_password = PasswordField('New Password', validators=[EqualTo('confirm_new_password', message='Passwords must match'), Optional()])
    confirm_new_password = PasswordField('Confirm New Password', validators=[Optional()])

class EditProfilePictureForm(FlaskForm):
    profile_image = FileField('Profile Image', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
