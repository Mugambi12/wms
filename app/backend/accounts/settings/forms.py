# app/backend/accounts/settings/forms.py

# Importing Required Libraries
from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, SubmitField, SelectField, IntegerField, TextAreaField
from wtforms.validators import Length, Email, URL

class CompanyInformationForm(FlaskForm):
    company_logo = StringField('Company Logo')
    company_name = StringField('Company Name')
    company_address = StringField('Company Address')
    company_email = StringField('Company Email', validators=[Email()])
    contact_number = StringField('Contact Number')
    company_website_url = StringField('Company Website URL', validators=[URL()])
    company_description = TextAreaField('Company Description')
    submit = SubmitField('Submit')





class UnitPriceForm(FlaskForm):
    unit_price = FloatField('Unit Price')
    submit = SubmitField('Submit')

class ServiceFeeForm(FlaskForm):
    service_fee = FloatField('Service Fees')
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



class BankNameForm(FlaskForm):
    bank_name = StringField('Bank Name')
    submit = SubmitField('Submit')

class PayBillForm(FlaskForm):
    paybill = IntegerField('PayBill Number')
    submit = SubmitField('Submit')

class AccountNumberForm(FlaskForm):
    account_number = IntegerField('Account Number')
    submit = SubmitField('Submit')

class ContactNumberForm(FlaskForm):
    contact_number = IntegerField('Contant Number', validators=[Length(min=9, max=20)])
    submit = SubmitField('Submit')
