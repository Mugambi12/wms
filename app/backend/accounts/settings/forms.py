# app/backend/accounts/settings/forms.py
from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class UnitPriceForm(FlaskForm):
    unit_price = FloatField('Unit Price', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ServiceFeeForm(FlaskForm):
    service_fee = FloatField('Unit Price', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AddHouseSectionForm(FlaskForm):
    house_sections = StringField('New House Section')
    submit = SubmitField()

class EditHouseSectionForm(FlaskForm):
    house_sections = SelectField('Select House Section', choices=[], coerce=str)
    new_house_section = StringField('New House Section Name')
    submit = SubmitField()

class DeleteHouseSectionForm(FlaskForm):
    house_sections = SelectField('Select House Section to Delete', choices=[], coerce=str)
    submit = SubmitField()

