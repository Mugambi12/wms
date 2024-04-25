from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, Email

class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[InputRequired()])
    email = StringField('Email Address', validators=[InputRequired(), Email()])
    message = TextAreaField('Your Message', validators=[InputRequired()])
