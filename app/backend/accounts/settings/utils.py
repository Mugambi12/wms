# app/backend/accounts/settings/routes.py
from flask import flash, redirect, url_for
from app import db
from ...database.models import Settings, CompanyInformation

def get_system_settings():
    general = Settings.query.first()
    return general

def update_company_name(system_settings, new_company_name):
    try:
        if system_settings is not None:
            if new_company_name is None:
                if system_settings.company_name is not None:
                    system_settings.company_name = None
                    db.session.commit()
                    flash('Company name removed successfully!', 'success')
                else:
                    flash('Company name is already empty.', 'info')
            else:
                system_settings.company_name = new_company_name
                db.session.commit()
                flash(f'Company name updated to "{new_company_name}" successfully!', 'success')
        else:
            if new_company_name is not None:
                new_settings = Settings(company_name=new_company_name)
                db.session.add(new_settings)
                db.session.commit()
                flash(f'Company name set to "{new_company_name}" successfully!', 'success')
            else:
                flash('Failed to update company name. No system settings found.', 'danger')

    except ValueError:
        flash('Invalid input for company name. Please enter a valid name.', 'danger')

def update_unit_price(system_settings, new_unit_price):
    try:
        if system_settings:
            if new_unit_price is None:
                if system_settings.unit_price is not None:
                    system_settings.unit_price = None
                    db.session.commit()
                    flash('Service fee removed successfully!', 'success')
            else:
                new_unit_price = float(new_unit_price)
                if system_settings.unit_price is not None:
                    system_settings.unit_price = new_unit_price
                    flash(f'Service fee updated to {new_unit_price} successfully!', 'success')
                else:
                    system_settings.unit_price = new_unit_price
                    flash(f'Service fee added as {new_unit_price} successfully!', 'success')
                db.session.commit()
        else:
            if new_unit_price is not None:
                new_unit_price = float(new_unit_price)
                new_settings = Settings(unit_price=new_unit_price)
                db.session.add(new_settings)
                db.session.commit()
                flash(f'Service fee added as {new_unit_price} successfully!', 'success')
            else:
                flash('Failed to add service fee. No system settings found.', 'danger')

    except ValueError:
        flash('Invalid input for service fee. Please enter a valid number.', 'danger')

def update_service_fee(system_settings, new_service_fee):
    try:
        if system_settings:
            if new_service_fee is None:
                if system_settings.service_fee is not None:
                    system_settings.service_fee = None
                    db.session.commit()
                    flash('Service fee removed successfully!', 'success')
            else:
                new_service_fee = float(new_service_fee)
                if system_settings.service_fee is not None:
                    system_settings.service_fee = new_service_fee
                    flash(f'Service fee updated to {new_service_fee} successfully!', 'success')
                else:
                    system_settings.service_fee = new_service_fee
                    flash(f'Service fee added as {new_service_fee} successfully!', 'success')
                db.session.commit()
        else:
            if new_service_fee is not None:
                new_service_fee = float(new_service_fee)
                new_settings = Settings(service_fee=new_service_fee)
                db.session.add(new_settings)
                db.session.commit()
                flash(f'Service fee added as {new_service_fee} successfully!', 'success')
            else:
                flash('Failed to add service fee. No system settings found.', 'danger')

    except ValueError:
        flash('Invalid input for service fee. Please enter a valid number.', 'danger')

def add_house_section(system_settings, house_section):
    if house_section:
        if system_settings:
            existing_sections = system_settings.house_sections.split(',') if system_settings.house_sections else []
            if house_section not in existing_sections:
                existing_sections.append(house_section)
                system_settings.house_sections = ','.join(existing_sections)
                db.session.commit()
                flash(f'House section "{house_section.title()}" added successfully!', 'success')
            else:
                flash(f'Failed to add house section. The section "{house_section.title()}" already exists.', 'danger')
        else:
            flash('Failed to add house section. System settings not found.', 'danger')
    else:
        flash('Failed to add house section. The provided house section is empty.', 'danger')

    return redirect(url_for('accounts.settings.settings'))

def edit_house_section(system_settings, selected_section, new_house_section):
    if new_house_section:
        if system_settings:
            house_sections = system_settings.house_sections.split(',') if system_settings.house_sections else []
            if selected_section in house_sections:
                house_sections.remove(selected_section)
                house_sections.append(new_house_section)
                system_settings.house_sections = ','.join(house_sections)
                db.session.commit()
                flash(f'House section "{selected_section.title()}" updated to "{new_house_section.title()}" successfully!', 'success')
            else:
                flash(f'Failed to update house section. The selected section "{selected_section.title()}" does not exist.', 'danger')
        else:
            flash('Failed to update house section. System settings not found.', 'danger')
    else:
        flash('Failed to update house section. The new house section is empty.', 'danger')

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

def update_bank_name(system_settings, new_bank_name):
    try:
        if system_settings:
            if new_bank_name is None:
                if system_settings.bank_name is not None:
                    system_settings.bank_name = None
                    db.session.commit()
                    flash('Company name removed successfully!', 'success')
                else:
                    flash('Company name is already empty.', 'info')
            else:
                system_settings.bank_name = new_bank_name
                db.session.commit()
                flash(f'Company name updated to "{new_bank_name}" successfully!', 'success')
        else:
            if new_bank_name is not None:
                new_settings = Settings(bank_name=new_bank_name)
                db.session.add(new_settings)
                db.session.commit()
                flash(f'Company name set to "{new_bank_name}" successfully!', 'success')
            else:
                flash('Failed to update company name. No system settings found.', 'danger')

    except ValueError:
        flash('Invalid input for company name. Please enter a valid name.', 'danger')

def update_paybill(system_settings, new_paybill):
    try:
        if system_settings:
            if new_paybill is None:
                if system_settings.paybill is not None:
                    system_settings.paybill = None
                    db.session.commit()
                    flash('Service fee removed successfully!', 'success')
            else:
                new_paybill = int(new_paybill)
                if system_settings.paybill is not None:
                    system_settings.paybill = new_paybill
                    flash(f'Service fee updated to {new_paybill} successfully!', 'success')
                else:
                    system_settings.paybill = new_paybill
                    flash(f'Service fee added as {new_paybill} successfully!', 'success')
                db.session.commit()
        else:
            if new_paybill is not None:
                new_paybill = int(new_paybill)
                new_settings = Settings(paybill=new_paybill)
                db.session.add(new_settings)
                db.session.commit()
                flash(f'Service fee added as {new_paybill} successfully!', 'success')
            else:
                flash('Failed to add service fee. No system settings found.', 'danger')

    except ValueError:
        flash('Invalid input for service fee. Please enter a valid number.', 'danger')

def update_account_number(system_settings, new_account_number):
    try:
        if system_settings:
            if new_account_number is None:
                if system_settings.account_number is not None:
                    system_settings.account_number = None
                    db.session.commit()
                    flash('Service fee removed successfully!', 'success')
            else:
                new_account_number = int(new_account_number)
                if system_settings.account_number is not None:
                    system_settings.account_number = new_account_number
                    flash(f'Service fee updated to {new_account_number} successfully!', 'success')
                else:
                    system_settings.account_number = new_account_number
                    flash(f'Service fee added as {new_account_number} successfully!', 'success')
                db.session.commit()
        else:
            if new_account_number is not None:
                new_account_number = int(new_account_number)
                new_settings = Settings(account_number=new_account_number)
                db.session.add(new_settings)
                db.session.commit()
                flash(f'Service fee added as {new_account_number} successfully!', 'success')
            else:
                flash('Failed to add service fee. No system settings found.', 'danger')

    except ValueError:
        flash('Invalid input for service fee. Please enter a valid number.', 'danger')

def update_contact_number(system_settings, new_contact_number):
    try:
        if system_settings:
            if new_contact_number is None:
                if system_settings.contact_number is not None:
                    system_settings.contact_number = None
                    db.session.commit()
                    flash('Service fee removed successfully!', 'success')
            else:
                new_contact_number = int(new_contact_number)
                if system_settings.contact_number is not None:
                    system_settings.contact_number = new_contact_number
                    flash(f'Service fee updated to {new_contact_number} successfully!', 'success')
                else:
                    system_settings.contact_number = new_contact_number
                    flash(f'Service fee added as {new_contact_number} successfully!', 'success')
                db.session.commit()
        else:
            if new_contact_number is not None:
                new_contact_number = int(new_contact_number)
                new_settings = Settings(contact_number=new_contact_number)
                db.session.add(new_settings)
                db.session.commit()
                flash(f'Service fee added as {new_contact_number} successfully!', 'success')
            else:
                flash('Failed to add service fee. No system settings found.', 'danger')

    except ValueError:
        flash('Invalid input for service fee. Please enter a valid number.', 'danger')
