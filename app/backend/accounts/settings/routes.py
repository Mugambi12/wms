# app/backend/accounts/settings/routes.py

import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required
from .forms import CompanyInformationForm
from app import db
from ...database.models import CompanyInformation


settings_bp = Blueprint('settings', __name__, url_prefix='/settings')


def get_company_information():
    return CompanyInformation.query.first()


def save_uploaded_logo(company_logo):
    if not company_logo:
        return None

    try:
        filename = secure_filename(company_logo.filename)
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

    return render_template('accounts/settings.html',
                           company_information=company_information,
                           company_information_form=company_information_form,
                           hide_footer=True)
