# app/backend/accounts/settings/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from .forms import CompanyNameForm, UnitPriceForm, ServiceFeeForm, AddHouseSectionForm, EditHouseSectionForm, DeleteHouseSectionForm, BankNameForm, PayBillForm, AccountNumberForm, ContactNumberForm
from .utils import get_system_settings, update_company_name, update_unit_price, update_service_fee, add_house_section, edit_house_section, delete_house_section, update_bank_name, update_paybill, update_account_number, update_contact_number


settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

from app import db
from app.backend.database.models import CompanyInformation

def update_company_information(system_settings, form_data):
    try:
        if system_settings:
            for field, value in form_data.items():
                if hasattr(system_settings, field):
                    setattr(system_settings, field, value)
            db.session.commit()
            flash('Company information updated successfully!', 'success')
        else:
            new_settings = CompanyInformation(**form_data)
            db.session.add(new_settings)
            db.session.commit()
            flash('Company information set successfully!', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Failed to update company information: {str(e)}', 'danger')




import os
from werkzeug.utils import secure_filename

def get_company_information():
    company_information = CompanyInformation.query.first()
    return company_information

# Function to handle file upload
def upload_logo(company_logo):
    if 'company_logo' in request.files:
        try:
            filename = secure_filename("company_logo.png")
            uploads_folder = os.path.join(current_app.root_path, 'frontend', 'static', 'uploads', 'tmp')
            save_path = os.path.join(uploads_folder, filename)
            company_logo.save(save_path)
            CompanyInformation.company_logo = url_for('static', filename=f'uploads/tmp/{filename}')
            db.session.commit()
            return True
        except Exception as e:
            print(f'Error saving company logo: {str(e)}')
            return False
    else:
        return False  # Return False if no file uploaded

@settings_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    company_name_form = CompanyNameForm()
    unit_price_form = UnitPriceForm()
    service_fee_form = ServiceFeeForm()
    add_section_form = AddHouseSectionForm()
    edit_section_form = EditHouseSectionForm()
    delete_section_form = DeleteHouseSectionForm()
    bank_name_form = BankNameForm()
    paybill_form = PayBillForm()
    account_number_form = AccountNumberForm()
    contact_number_form = ContactNumberForm()

    system_settings = get_system_settings()
    company_information = get_company_information()
    company_name_form.process(obj=company_information)

    if company_information:
        company_name_form.company_logo.data = company_information.company_logo
        company_name_form.company_name.data = company_information.company_name
        company_name_form.company_address.data = company_information.company_address
        company_name_form.company_email.data = company_information.company_email
        company_name_form.contact_number.data = company_information.contact_number
        company_name_form.company_website_url.data = company_information.company_website_url
        company_name_form.company_description.data = company_information.company_description

    if system_settings:
        unit_price_form.unit_price.data = system_settings.unit_price
        service_fee_form.service_fee.data = system_settings.service_fee
        house_sections = system_settings.house_sections.split(',') if system_settings.house_sections else []
        edit_section_form.house_sections.choices = [(section, section) for section in house_sections]
        delete_section_form.house_sections.choices = [(section, section) for section in house_sections]
        bank_name_form.bank_name.data = system_settings.bank_name
        paybill_form.paybill.data = system_settings.paybill
        account_number_form.account_number.data = system_settings.account_number
        contact_number_form.contact_number.data = system_settings.contact_number

    if request.method == 'POST':
        if 'company_information_submit' in request.form:
            # Handle file upload separately and update company information
            company_logo = request.files.get('company_logo')
            if upload_logo(company_logo):
                form_data = {
                    'company_name': company_name_form.company_name.data,
                    'company_address': company_name_form.company_address.data,
                    'company_email': company_name_form.company_email.data,
                    'contact_number': company_name_form.contact_number.data,
                    'company_website_url': company_name_form.company_website_url.data,
                    'company_description': company_name_form.company_description.data
                }
                update_company_information(company_information, form_data)
            else:
                flash('Error uploading company logo', 'danger')
            return redirect(url_for('accounts.settings.settings'))

        #elif 'company_name_submit' in request.form:
        #    update_company_name(system_settings, company_name_form.company_name.data)
        #    return redirect(url_for('accounts.settings.settings'))

        elif 'unit_price_submit' in request.form:
            update_unit_price(system_settings, unit_price_form.unit_price.data)
            return redirect(url_for('accounts.settings.settings'))

        elif 'service_fee_submit' in request.form:
            update_service_fee(system_settings, service_fee_form.service_fee.data)
            return redirect(url_for('accounts.settings.settings'))

        elif 'add_section_submit' in request.form and add_section_form.validate_on_submit():
            return add_house_section(system_settings, add_section_form.house_sections.data)

        elif 'edit_section_submit' in request.form and edit_section_form.validate_on_submit():
            return edit_house_section(system_settings, edit_section_form.house_sections.data, edit_section_form.new_house_section.data)

        elif 'delete_section_submit' in request.form and delete_section_form.validate_on_submit():
            return delete_house_section(system_settings, delete_section_form.house_sections.data)

        elif 'bank_name_submit' in request.form:
            update_bank_name(system_settings, bank_name_form.bank_name.data)
            return redirect(url_for('accounts.settings.settings'))

        elif 'paybill_submit' in request.form:
            update_paybill(system_settings, paybill_form.paybill.data)
            return redirect(url_for('accounts.settings.settings'))

        elif 'account_number_submit' in request.form:
            update_account_number(system_settings, account_number_form.account_number.data)
            return redirect(url_for('accounts.settings.settings'))

        elif 'contact_number_submit' in request.form:
            update_contact_number(system_settings, contact_number_form.contact_number.data)
            return redirect(url_for('accounts.settings.settings'))

        flash('There was an error!', 'danger')
        return redirect(url_for('accounts.settings.settings'))

    return render_template('accounts/settings.html',
                           company_information=company_information,

                           company_name_form=company_name_form,
                           unit_price_form=unit_price_form,
                           service_fee_form=service_fee_form,
                           add_section_form=add_section_form,
                           edit_section_form=edit_section_form,
                           delete_section_form=delete_section_form,
                           bank_name_form=bank_name_form,
                           paybill_form=paybill_form,
                           account_number_form=account_number_form,
                           contact_number_form=contact_number_form,
                           hide_footer=True)
