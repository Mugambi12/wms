import os
from werkzeug.utils import secure_filename
from flask import redirect, url_for, flash, current_app
from core import db
from ...database.models import CompanyInformation, ServicesSetting, PaymentMethods, MailSettings, SocialAccounts


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
