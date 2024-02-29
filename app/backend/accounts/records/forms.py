from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, BooleanField, SubmitField, DateField, DateTimeField, DateTimeLocalField
from wtforms.validators import DataRequired

class AddMeterReadingForm(FlaskForm):
    house_section = StringField('House Section:', validators=[DataRequired()])
    house_number = StringField('House Number:', validators=[DataRequired()])
    reading_value = FloatField('Reading Value:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditMeterReadingForm(FlaskForm):
    customer_name = StringField('Customer Name', validators=[DataRequired()])
    house_section = StringField('House Section', validators=[DataRequired()])
    house_number = StringField('House Number', validators=[DataRequired()])
    reading_value = FloatField('Reading Value', validators=[DataRequired()])
    consumed = FloatField('Consumed Units', validators=[DataRequired()])
    unit_price = FloatField('Unit Price', validators=[DataRequired()])
    total_amount = FloatField('Total Price', validators=[DataRequired()])
    timestamp = DateField('Reading Date', validators=[DataRequired()])
    submit = SubmitField('Update')


from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SelectField, IntegerField
from wtforms.validators import InputRequired, NumberRange, Optional

class MakePaymentForm(FlaskForm):
    payment_amount = FloatField('Paid Amount', validators=[InputRequired(), NumberRange(min=0)])
    payment_method = SelectField('Payment Method', choices=[('m_pesa', 'M-Pesa'), ('bank_transfer', 'Bank Transfer'), ('debit_card', 'Debit Card'), ('credit_card', 'Credit Card'), ('paypal', 'PayPal')], validators=[InputRequired()])
    reference_number = StringField('Reference Number', validators=[Optional()])
    status = BooleanField('Payment Status', default=False)
