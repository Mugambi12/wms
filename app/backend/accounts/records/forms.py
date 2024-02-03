from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, DateField, BooleanField, SubmitField, DateTimeField
from wtforms.validators import DataRequired

class AddMeterReadingForm(FlaskForm):
    house_section = StringField('House Section:', validators=[DataRequired()])
    house_number = StringField('House Number:', validators=[DataRequired()])
    reading_value = FloatField('Reading Value:', validators=[DataRequired()])
    timestamp = DateField('Reading Date', validators=[DataRequired()])
    reading_status = BooleanField('Reading Status')
    submit = SubmitField('Submit')


class EditMeterReadingForm(FlaskForm):
    house_section = StringField('House Section', validators=[DataRequired()])
    house_number = StringField('House Number', validators=[DataRequired()])
    reading_value = FloatField('Reading Value', validators=[DataRequired()])
    timestamp = DateField('Reading Date', validators=[DataRequired()])
    reading_status = BooleanField('Reading Status')
    submit = SubmitField('Update')

