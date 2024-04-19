from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, BooleanField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Optional


class AddMeterReadingForm(FlaskForm):
    house_section = StringField('House Section:', validators=[DataRequired()])
    house_number = StringField('House Number:', validators=[DataRequired()])
    reading_value = FloatField('Reading Value:', validators=[InputRequired()])
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


class MakePaymentForm(FlaskForm):
    payment_amount = FloatField('Paid Amount', validators=[InputRequired(), NumberRange(min=0)])
    payment_method = SelectField('Payment Method', choices=[('m_pesa', 'M-Pesa'), ('bank_transfer', 'Bank Transfer'), ('paypal', 'PayPal')], validators=[InputRequired()])
    reference_number = StringField('Reference Number', validators=[Optional()])
    status = BooleanField('Payment Status', default=False)


class EditPaymentForm(FlaskForm):
    payment_method = SelectField('Payment Method', choices=[('m_pesa', 'M-Pesa'), ('bank_transfer', 'Bank Transfer'), ('paypal', 'PayPal')], validators=[InputRequired()])
    amount = FloatField('Paid Amount', validators=[InputRequired(), NumberRange(min=0)])
    reference_number = StringField('Reference Number', validators=[Optional()])
    timestamp = DateField('Reading Date', validators=[DataRequired()])
