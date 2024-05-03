from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, SubmitField, TextAreaField, PasswordField, FileField
from wtforms.validators import Email, URL, DataRequired, Optional


class CompanyInformationForm(FlaskForm):
    company_logo = FileField('Company Logo')
    company_name = StringField('Company Name', validators=[DataRequired()])
    company_address = StringField('Company Address')
    company_email = StringField('Company Email', validators=[Email()])
    contact_number = StringField('Contact Number')
    company_website_url = StringField('Company Website URL', validators=[URL()])
    company_description = TextAreaField('Company Description')
    submit = SubmitField('Submit')


class ServicesSettingForm(FlaskForm):
    unit_price = FloatField('Unit Price')
    service_fee = FloatField('Service Fee')
    submit = SubmitField('Update')


class AddHouseSectionForm(FlaskForm):
    house_sections = StringField('New House Section')
    submit = SubmitField()


class EditSectionForm(FlaskForm):
    edit_house_section = StringField('Edit House Section', validators=[DataRequired()])
    new_section_name = StringField('New Section Name', validators=[DataRequired()])
    submit = SubmitField('Edit')


class PaymentMethodsForm(FlaskForm):
    bank_name = StringField('Bank Name')
    paybill = StringField('Pay Bill Number')
    account_number = StringField('Account Number')
    submit = SubmitField('Update')


class MailSettingsForm(FlaskForm):
    mail_server = StringField('Mail Sever')
    company_email = StringField('Email Address', validators=[Email(), Optional()])
    password = PasswordField('Email Password')
    submit = SubmitField('Update')


class SocialAccountsForm(FlaskForm):
    whatsapp = StringField('WhatsApp')
    twitter = StringField('Twitter')
    facebook = StringField('Facebook')
    tiktok = StringField('TikTok')
    instagram = StringField('Instagram')
    linkedin = StringField('LinkedIn')
    youtube = StringField('YouTube')
