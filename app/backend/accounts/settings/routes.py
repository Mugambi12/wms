# app/backend/accounts/settings/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from .forms import UnitPriceForm, AddHouseSectionForm, EditHouseSectionForm, DeleteHouseSectionForm
from ...models.user import Settings

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

def get_system_settings():
    return Settings.query.first()

def update_unit_price(system_settings, new_unit_price):
    if system_settings:
        if system_settings.unit_price is not None:
            system_settings.unit_price = None
            db.session.commit()

        system_settings.unit_price = new_unit_price
        db.session.commit()
        flash(f'Unit Price updated to "{new_unit_price.title()}" successfully!', 'success')

    else:
        new_settings = Settings(unit_price=new_unit_price)
        db.session.add(new_settings)
        db.session.commit()
        flash(f'Unit Price added as "{new_unit_price.title()}" successfully!', 'success')

def add_house_section(system_settings, house_section):
    if system_settings:
        existing_sections = system_settings.house_sections.split(',') if system_settings.house_sections else []
        if house_section not in existing_sections:
            existing_sections.append(house_section)
            system_settings.house_sections = ','.join(existing_sections)
            db.session.commit()
            flash(f'House section "{house_section.title()}" added successfully!', 'success')

    return redirect(url_for('accounts.settings.settings'))

def edit_house_section(system_settings, selected_section, new_house_section):
    if system_settings:
        house_sections = system_settings.house_sections.split(',') if system_settings.house_sections else []
        if selected_section in house_sections:
            house_sections.remove(selected_section)
            house_sections.append(new_house_section)
            system_settings.house_sections = ','.join(house_sections)
            db.session.commit()
            flash(f'House section "{selected_section.title()}" updated to "{new_house_section.title()}" successfully!', 'success')

    return redirect(url_for('accounts.settings.settings'))

def delete_house_section(system_settings, selected_section):
    if system_settings:
        house_sections = system_settings.house_sections.split(',') if system_settings.house_sections else []
        if selected_section in house_sections:
            house_sections.remove(selected_section)
            system_settings.house_sections = ','.join(house_sections)
            db.session.commit()
            flash(f'House section "{selected_section.title()}" deleted successfully!', 'success')

    return redirect(url_for('accounts.settings.settings'))

@settings_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    unit_price_form = UnitPriceForm()
    add_section_form = AddHouseSectionForm()
    edit_section_form = EditHouseSectionForm()
    delete_section_form = DeleteHouseSectionForm()

    system_settings = get_system_settings()
    new_unit_price = unit_price_form.unit_price.data

    if system_settings:
        unit_price_form.unit_price.data = system_settings.unit_price
        house_sections = system_settings.house_sections.split(',') if system_settings.house_sections else []
        edit_section_form.house_sections.choices = [(section, section) for section in house_sections]
        delete_section_form.house_sections.choices = [(section, section) for section in house_sections]

    if request.method == 'POST':
        if 'unit_price_submit' in request.form:
            update_unit_price(system_settings, new_unit_price)
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
                           unit_price_form=unit_price_form,
                           add_section_form=add_section_form,
                           edit_section_form=edit_section_form,
                           delete_section_form=delete_section_form,
                           hide_footer=True)
