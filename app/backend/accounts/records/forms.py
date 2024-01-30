# app/backend/accounts/records/forms.py
from flask_wtf import FlaskForm
from wtforms import FloatField, DateField, StringField, SubmitField
from wtforms.validators import DataRequired

class AddMeterReadingForm(FlaskForm):
    reading_value = FloatField('Reading Value', validators=[DataRequired()])
    reading_date = DateField('Reading Date', validators=[DataRequired()])
    house_section = StringField('House Section', validators=[DataRequired()])
    house_number = StringField('House Number', validators=[DataRequired()])
    submit = SubmitField('Submit')
