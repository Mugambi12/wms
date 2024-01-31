# app/backend/accounts/records/forms.py
from flask_wtf import FlaskForm
from wtforms import FloatField, DateField, StringField, SubmitField
from wtforms.validators import DataRequired

class AddMeterReadingForm(FlaskForm):
    house_section = StringField('House Section', validators=[DataRequired()])
    house_number = StringField('House Number', validators=[DataRequired()])
    reading_date = DateField('Reading Date', validators=[DataRequired()])
    reading_value = FloatField('Reading Value', validators=[DataRequired()])
    submit = SubmitField('Submit')
