# app/backend/accounts/settings/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from .forms import CompanyNameForm, UnitPriceForm, ServiceFeeForm, AddHouseSectionForm, EditHouseSectionForm, DeleteHouseSectionForm
from .settings import get_system_settings, update_company_name, update_unit_price, update_service_fee, add_house_section, edit_house_section, delete_house_section


settings_bp = Blueprint('settings', __name__, url_prefix='/settings')


@settings_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    company_name_form = CompanyNameForm()
    unit_price_form = UnitPriceForm()
    service_fee_form = ServiceFeeForm()
    add_section_form = AddHouseSectionForm()
    edit_section_form = EditHouseSectionForm()
    delete_section_form = DeleteHouseSectionForm()

    system_settings = get_system_settings()
    new_company_name = company_name_form.company_name.data
    new_unit_price = unit_price_form.unit_price.data
    new_service_fee = service_fee_form.service_fee.data

    if system_settings:
        company_name_form.company_name.data = system_settings.company_name
        unit_price_form.unit_price.data = system_settings.unit_price
        service_fee_form.service_fee.data = system_settings.service_fee
        house_sections = system_settings.house_sections.split(',') if system_settings.house_sections else []
        edit_section_form.house_sections.choices = [(section, section) for section in house_sections]
        delete_section_form.house_sections.choices = [(section, section) for section in house_sections]

    if request.method == 'POST':
        if 'company_name_submit' in request.form:
            update_company_name(system_settings, new_company_name)
            return redirect(url_for('accounts.settings.settings'))

        elif 'unit_price_submit' in request.form:
            update_unit_price(system_settings, new_unit_price)
            return redirect(url_for('accounts.settings.settings'))

        elif 'service_fee_submit' in request.form:
            update_service_fee(system_settings, new_service_fee)
            return redirect(url_for('accounts.settings.settings'))

        elif 'add_section_submit' in request.form and add_section_form.validate_on_submit():
            return add_house_section(system_settings, add_section_form.house_sections.data)

        elif 'edit_section_submit' in request.form and edit_section_form.validate_on_submit():
            return edit_house_section(system_settings, edit_section_form.house_sections.data, edit_section_form.new_house_section.data)

        elif 'delete_section_submit' in request.form and delete_section_form.validate_on_submit():
            return delete_house_section(system_settings, delete_section_form.house_sections.data)

        flash(f'There was an error!', 'danger')
        return redirect(url_for('accounts.settings.settings'))

    return render_template('accounts/settings.html',
                           company_name_form=company_name_form,
                           unit_price_form=unit_price_form,
                           service_fee_form=service_fee_form,
                           add_section_form=add_section_form,
                           edit_section_form=edit_section_form,
                           delete_section_form=delete_section_form,
                           hide_footer=True)
