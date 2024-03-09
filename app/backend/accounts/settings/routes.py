import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required
from .forms import CompanyInformationForm, ServicesSettingForm, PaymentMethodsForm, MailSettingsForm, SocialAccountsForm
from app import db
from ...database.models import CompanyInformation, ServicesSetting, PaymentMethods, MailSettings, SocialAccounts

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

def get_company_information():
    return CompanyInformation.query.first()

def save_uploaded_logo(company_logo):
    if not company_logo:
        return None

    try:
        filename = secure_filename("company_logo.png")
        uploads_folder = os.path.join(current_app.root_path, 'frontend', 'static', 'uploads', 'tmp')
        save_path = os.path.join(uploads_folder, filename)
        company_logo.save(save_path)
        return url_for('static', filename=f'uploads/tmp/{filename}')
    except Exception as e:
        print(f'Error saving company logo: {str(e)}')
        return None

def update_or_create_company_information(company_information, form_data):
    try:
        if company_information:
            for field, value in form_data.items():
                if hasattr(company_information, field):
                    setattr(company_information, field, value)
        else:
            company_information = CompanyInformation(**form_data)
            db.session.add(company_information)

        db.session.commit()
        flash('Company information updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Failed to update company information: {str(e)}', 'danger')

@settings_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    company_information = get_company_information()
    company_information_form = CompanyInformationForm(obj=company_information)

    if company_information_form.validate_on_submit():
        company_logo = request.files.get('company_logo')
        logo_url = save_uploaded_logo(company_logo)

        form_data = {
            'company_logo': logo_url,
            'company_name': company_information_form.company_name.data,
            'company_address': company_information_form.company_address.data,
            'company_email': company_information_form.company_email.data,
            'contact_number': company_information_form.contact_number.data,
            'company_website_url': company_information_form.company_website_url.data,
            'company_description': company_information_form.company_description.data
        }

        update_or_create_company_information(company_information, form_data)

        return redirect(url_for('accounts.settings.settings'))

    service_settings = get_service_settings()
    section_settings = get_section_settings()
    all_house_sections = []

    if section_settings:
        all_house_sections = section_settings.house_sections.split(',') if section_settings.house_sections else []

    payment_methods = get_payment_methods()
    mail_settings = get_mail_settings()
    social_accounts = get_social_accounts()

    return render_template('accounts/settings.html',
                           company_information=company_information,
                           company_information_form=company_information_form,
                           service_settings=service_settings,
                           all_house_sections=all_house_sections,
                           payment_methods=payment_methods,
                           mail_settings=mail_settings,
                           social_accounts=social_accounts,
                           hide_footer=True)


def get_service_settings():
    return ServicesSetting.query.first()

def update_or_create_service_settings(service_settings, form_data):
    try:
        if service_settings:
            for field, value in form_data.items():
                setattr(service_settings, field, value)
            db.session.commit()
            flash('Service settings updated successfully!', 'success')
        else:
            new_service_settings = ServicesSetting(**form_data)
            db.session.add(new_service_settings)
            db.session.commit()
            flash('Service settings set successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Failed to update service settings: {str(e)}', 'danger')

@settings_bp.route('/service_settings', methods=['GET', 'POST'])
@login_required
def service_settings():
    service_settings_form = ServicesSettingForm()
    service_settings = get_service_settings()

    if service_settings:
        service_settings_form = ServicesSettingForm(obj=service_settings)

    if service_settings_form.validate_on_submit():
        form_data = {
            'unit_price': service_settings_form.unit_price.data,
            'service_fee': service_settings_form.service_fee.data
        }

        update_or_create_service_settings(service_settings, form_data)

        return redirect(url_for('accounts.settings.settings'))

    return redirect(url_for('accounts.settings.settings'))


from .forms import AddHouseSectionForm

def get_section_settings():
    return ServicesSetting.query.first()

def add_house_section(all_house_sections, house_section):
    if not house_section:
        flash('Failed to add house section. The provided house section is empty.', 'danger')
        return redirect(url_for('accounts.settings.settings'))

    existing_sections = all_house_sections.house_sections.split(',') if all_house_sections.house_sections else []
    if house_section in existing_sections:
        flash(f'Failed to add house section. The section "{house_section.title()}" already exists.', 'danger')
        return redirect(url_for('accounts.settings.settings'))

    existing_sections.append(house_section)
    all_house_sections.house_sections = ','.join(existing_sections)
    db.session.commit()
    flash(f'House section "{house_section.title()}" added successfully!', 'success')
    return redirect(url_for('accounts.settings.settings'))

@settings_bp.route('/add_section', methods=['POST'])
@login_required
def add_section():
    add_section_form = AddHouseSectionForm()
    if add_section_form.validate_on_submit():
        house_section = add_section_form.house_sections.data.strip()
        service_settings = get_section_settings()
        return add_house_section(service_settings, house_section)

    flash('Failed to add house section. Please check your input.', 'danger')
    return redirect(url_for('accounts.settings.settings'))



from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class EditSectionForm(FlaskForm):
    edit_house_section = StringField('Edit House Section', validators=[DataRequired()])
    new_section_name = StringField('New Section Name', validators=[DataRequired()])
    submit = SubmitField('Edit')


@settings_bp.route('/edit_section', methods=['POST'])
@login_required
def edit_section():
    edited_section = request.form.get('edit_house_section')
    new_section_name = request.form.get('new_section_name')

    if not edited_section:
        flash('Please select a section to edit.', 'danger')
        return redirect(url_for('accounts.settings.settings'))

    if not new_section_name:
        flash('Please provide a new name for the section.', 'danger')
        return redirect(url_for('accounts.settings.settings'))

    # Here you can perform any necessary validation or processing of the edited section
    # For example, you might directly update the section in your database

    try:
        # Update the section name in the database
        services_setting = ServicesSetting.query.first()
        if services_setting:
            house_sections = services_setting.house_sections.split(',')
            if edited_section in house_sections:
                house_sections[house_sections.index(edited_section)] = new_section_name
                services_setting.house_sections = ','.join(house_sections)
                db.session.commit()
                flash(f'Successfully edited section: {edited_section} to {new_section_name}', 'success')
            else:
                flash(f'Section "{edited_section}" not found.', 'danger')
        else:
            flash('No service settings found.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Failed to edit section: {str(e)}', 'danger')

    return redirect(url_for('accounts.settings.settings'))




@settings_bp.route('/delete_section', methods=['POST'])
@login_required
def delete_section():
    deleted_section_name = request.form.get('delete_house_section')
    if not deleted_section_name:
        flash('Please select a section to delete.', 'danger')
        return redirect(url_for('accounts.settings.settings'))

    # Query the ServicesSetting object
    services_setting = ServicesSetting.query.first()
    if not services_setting:
        flash('No service settings found.', 'danger')
        return redirect(url_for('accounts.settings.settings'))

    # Split the house sections and remove the deleted section
    house_sections = services_setting.house_sections.split(',')
    if deleted_section_name not in house_sections:
        flash(f'Section "{deleted_section_name}" not found.', 'danger')
        return redirect(url_for('accounts.settings.settings'))

    house_sections.remove(deleted_section_name)
    services_setting.house_sections = ','.join(house_sections)

    try:
        # Commit the changes to the database
        db.session.commit()
        flash(f'Successfully deleted section: {deleted_section_name}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Failed to delete section: {str(e)}', 'danger')

    # Redirect back to the settings page after deletion
    return redirect(url_for('accounts.settings.settings'))


















def get_payment_methods():
    return PaymentMethods.query.first()

def update_or_create_payment_methods(payment_methods, form_data):
    try:
        if payment_methods:
            for field, value in form_data.items():
                setattr(payment_methods, field, value)
            db.session.commit()
            flash('Payment methods updated successfully!', 'success')
        else:
            new_payment_methods = PaymentMethods(**form_data)
            db.session.add(new_payment_methods)
            db.session.commit()
            flash('Payment methods set successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Failed to update payment methods: {str(e)}', 'danger')

@settings_bp.route('/payment_methods', methods=['GET', 'POST'])
@login_required
def payment_methods():
    payment_methods_form = PaymentMethodsForm()
    payment_methods = get_payment_methods()

    if payment_methods:
        payment_methods_form = PaymentMethodsForm(obj=payment_methods)

    if payment_methods_form.validate_on_submit():
        form_data = {
            'bank_name': payment_methods_form.bank_name.data,
            'paybill': payment_methods_form.paybill.data,
            'account_number': payment_methods_form.account_number.data
        }

        update_or_create_payment_methods(payment_methods, form_data)

        return redirect(url_for('accounts.settings.settings'))

    return redirect(url_for('accounts.settings.settings'))




def get_mail_settings():
    return MailSettings.query.first()

def update_or_create_mail_settings(mail_settings, form_data):
    try:
        if mail_settings:
            for field, value in form_data.items():
                setattr(mail_settings, field, value)
            db.session.commit()
            flash('Mail settings updated successfully!', 'success')
        else:
            new_mail_settings = MailSettings(**form_data)
            db.session.add(new_mail_settings)
            db.session.commit()
            flash('Mail settings set successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Failed to update mail settings: {str(e)}', 'danger')

@settings_bp.route('/mail-settings', methods=['GET', 'POST'])
@login_required
def mail_settings():
    mail_settings_form = MailSettingsForm()
    mail_settings = get_mail_settings()

    if mail_settings:
        mail_settings_form = MailSettingsForm(obj=mail_settings)

    if mail_settings_form.validate_on_submit():
        form_data = {
            'company_email': mail_settings_form.company_email.data,
            'sending_email': mail_settings_form.sending_email.data,
            'password': mail_settings_form.password.data
        }

        update_or_create_mail_settings(mail_settings, form_data)

        return redirect(url_for('accounts.settings.settings'))

    return redirect(url_for('accounts.settings.settings'))



def get_social_accounts():
    return SocialAccounts.query.first()

def update_or_create_social_accounts(social_accounts, form_data):
    try:
        if social_accounts:
            for field, value in form_data.items():
                setattr(social_accounts, field, value)
            db.session.commit()
            flash('Social accounts updated successfully!', 'success')
        else:
            new_social_accounts = SocialAccounts(**form_data)
            db.session.add(new_social_accounts)
            db.session.commit()
            flash('Social accounts set successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Failed to update social accounts: {str(e)}', 'danger')

@settings_bp.route('/social_accounts', methods=['GET', 'POST'])
@login_required
def social_accounts():
    social_accounts_form = SocialAccountsForm()
    social_accounts = get_social_accounts()

    if social_accounts:
        social_accounts_form = SocialAccountsForm(obj=social_accounts)

    if social_accounts_form.validate_on_submit():
        form_data = {
            'whatsapp': social_accounts_form.whatsapp.data,
            'twitter': social_accounts_form.twitter.data,
            'facebook': social_accounts_form.facebook.data,
            'tiktok': social_accounts_form.tiktok.data,
            'instagram': social_accounts_form.instagram.data,
            'linkedin': social_accounts_form.linkedin.data
        }

        update_or_create_social_accounts(social_accounts, form_data)

        return redirect(url_for('accounts.settings.settings'))

    return redirect(url_for('accounts.settings.settings'))
