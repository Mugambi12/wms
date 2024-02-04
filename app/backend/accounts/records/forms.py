from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, BooleanField, SubmitField, DateField, DateTimeField, DateTimeLocalField
from wtforms.validators import DataRequired

class AddMeterReadingForm(FlaskForm):
    house_section = StringField('House Section:', validators=[DataRequired()])
    house_number = StringField('House Number:', validators=[DataRequired()])
    reading_value = FloatField('Reading Value:', validators=[DataRequired()])
    submit = SubmitField('Submit')



# Update the EditMeterReadingForm to handle default values
class EditMeterReadingForm(FlaskForm):
    house_section = StringField('House Section', validators=[DataRequired()])
    house_number = StringField('House Number', validators=[DataRequired()])
    reading_value = FloatField('Reading Value', validators=[DataRequired()])
    consumed = FloatField('Consumed Units', validators=[DataRequired()])
    unit_price = FloatField('Unit Price', validators=[DataRequired()])
    total_price = FloatField('Total Price', validators=[DataRequired()])
    timestamp = DateTimeField('Reading Date', validators=[DataRequired()])
    reading_status = BooleanField('Reading Status')
    submit = SubmitField('Update')
