# app/backend/accounts/settings/routes.py
from flask import flash, redirect, url_for
from app import db
from ...models.user import Settings

def get_system_settings():
    return Settings.query.first()

def update_company_name(system_settings, new_company_name):
    try:
        if system_settings:
            if system_settings.company_name is not None:
                system_settings.company_name = None
                db.session.commit()

            system_settings.company_name = new_company_name
            db.session.commit()
            flash(f'Company name updated to "{new_company_name}" successfully!', 'success')

        else:
            new_settings = Settings(company_name=new_company_name)
            db.session.add(new_settings)
            db.session.commit()
            flash(f'Company name set to "{new_company_name}" successfully!', 'success')

    except ValueError:
        flash('Invalid input for company name. Please enter a valid name.', 'danger')

def update_unit_price(system_settings, new_unit_price):
    try:
        new_unit_price = float(new_unit_price)

        if system_settings:
            if system_settings.unit_price is not None:
                system_settings.unit_price = None
                db.session.commit()

            system_settings.unit_price = new_unit_price
            db.session.commit()
            flash(f'Unit Price updated to "{new_unit_price}" successfully!', 'success')

        else:
            new_settings = Settings(unit_price=new_unit_price)
            db.session.add(new_settings)
            db.session.commit()
            flash(f'Unit Price added as "{new_unit_price}" successfully!', 'success')

    except ValueError:
        flash('Invalid input for Unit Price. Please enter a valid number.', 'danger')

def update_service_fee(system_settings, new_service_fee):
    try:
        new_service_fee = float(new_service_fee)

        if system_settings:
            if system_settings.service_fee is not None:
                system_settings.service_fee = None
                db.session.commit()
                flash(f'Service fee updated to {new_service_fee:.2f} successfully!', 'success')
            else:
                system_settings.service_fee = new_service_fee
                db.session.commit()
                flash(f'Service fee added as {new_service_fee:.2f} successfully!', 'success')
        else:
            new_settings = Settings(service_fee=new_service_fee)
            db.session.add(new_settings)
            db.session.commit()
            flash(f'Service fee added as {new_service_fee:.2f} successfully!', 'success')

    except ValueError:
        flash('Invalid input for service fee. Please enter a valid number.', 'danger')

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
