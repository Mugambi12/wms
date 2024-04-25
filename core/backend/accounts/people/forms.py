# app/backend/accounts/people/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, SelectField
from wtforms.validators import EqualTo, DataRequired, Email, Length, Optional, ValidationError
from flask_wtf.file import FileField, FileAllowed
from core.backend.database.models import User, ServicesSetting


class AddUserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    mobile_number = StringField('Mobile Number', validators=[DataRequired(), Length(min=10, max=20)])
    email = StringField('Email', validators=[Optional(), Length(max=50)])
    house_section = SelectField('House Section', validators=[DataRequired()], coerce=str)
    house_number = StringField('House Number', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_mobile_number(self, field):
        if User.query.filter_by(mobile_number=field.data).first():
            raise ValidationError('Mobile number is already registered.')


class EditUserForm(FlaskForm):
    first_name = StringField('First Name', validators=[Optional()])
    last_name = StringField('Last Name', validators=[Optional()])
    mobile_number = StringField('Mobile Number', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(), Optional()])
    house_section = SelectField('House Section', validators=[Optional()], choices=[], default="")
    house_number = StringField('House Number', validators=[DataRequired()])
    profile_image = StringField('Profile Image URL', validators=[Optional()])
    is_active = BooleanField('Active', validators=[Optional()])
    is_admin = BooleanField('Admin', validators=[Optional()])
    current_password = PasswordField('Current Password', validators=[Optional()])
    new_password = PasswordField('New Password', validators=[Optional(), Length(min=6), EqualTo('confirm_new_password', message='Passwords must match')])
    confirm_new_password = PasswordField('Confirm New Password', validators=[Optional()])

    def populate_house_sections(self):
        settings = ServicesSetting.query.first()
        if settings and settings.house_sections:
            current_house_section = self.house_section.data
            self.house_section.choices = [(section, section) for section in settings.house_sections.split(',')]
            self.house_section.data = current_house_section

    def set_admin_edit(self, admin_edit):
        if not admin_edit:
            self.house_section.validators = [Optional()]
            self.house_number.validators = [Optional()]


class EditProfilePictureForm(FlaskForm):
    profile_image = FileField('Profile Image', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
