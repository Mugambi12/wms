from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from core import db
from .forms import *
from .utils import *
from ...database.models import ServicesSetting


settings_bp = Blueprint('settings', __name__, url_prefix='/settings')


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
                           hide_footer=True,
                           title="Settings")


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


@settings_bp.route('/add_section', methods=['POST'])
@login_required
def add_section():
    add_section_form = AddHouseSectionForm()
    if add_section_form.validate_on_submit():
        house_section = add_section_form.house_sections.data.strip()
        section_settings = get_section_settings()

        if section_settings:
            return add_house_section(section_settings, house_section)
        else:
            flash('No section settings found. Please set up prices section above first.', 'danger')
            return redirect(url_for('accounts.settings.settings'))

    flash('Failed to add house section. Please check your input.', 'danger')
    return redirect(url_for('accounts.settings.settings'))


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

    try:
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

    services_setting = ServicesSetting.query.first()
    if not services_setting:
        flash('No service settings found.', 'danger')
        return redirect(url_for('accounts.settings.settings'))

    house_sections = services_setting.house_sections.split(',')
    if deleted_section_name not in house_sections:
        flash(f'Section "{deleted_section_name}" not found.', 'danger')
        return redirect(url_for('accounts.settings.settings'))

    house_sections.remove(deleted_section_name)
    services_setting.house_sections = ','.join(house_sections)

    try:
        db.session.commit()
        flash(f'Successfully deleted section: {deleted_section_name}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Failed to delete section: {str(e)}', 'danger')

    return redirect(url_for('accounts.settings.settings'))


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
            'mail_server': mail_settings_form.mail_server.data,
            'password': mail_settings_form.password.data
        }

        update_or_create_mail_settings(mail_settings, form_data)

        return redirect(url_for('accounts.settings.settings'))

    return redirect(url_for('accounts.settings.settings'))


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
            'linkedin': social_accounts_form.linkedin.data,
            'youtube': social_accounts_form.youtube.data
        }

        update_or_create_social_accounts(social_accounts, form_data)

        return redirect(url_for('accounts.settings.settings'))

    return redirect(url_for('accounts.settings.settings'))
