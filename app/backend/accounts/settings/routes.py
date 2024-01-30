# app/backend/accounts/settings/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required
from app import db
from .forms import UnitPriceForm, AddHouseSectionForm, EditHouseSectionForm, DeleteHouseSectionForm
from ...models.user import Settings

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

@settings_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    unit_price_form = UnitPriceForm()
    add_section_form = AddHouseSectionForm()
    edit_section_form = EditHouseSectionForm()
    delete_section_form = DeleteHouseSectionForm()

    system_settings = Settings.query.first()

    if system_settings:
        unit_price_form.unit_price.data = system_settings.unit_price
        house_sections = system_settings.house_sections.split(',') if system_settings.house_sections else []
        edit_section_form.house_sections.choices = [(section, section) for section in house_sections]
        delete_section_form.house_sections.choices = [(section, section) for section in house_sections]

    if request.method == 'POST':
        if 'unit_price_submit' in request.form and unit_price_form.validate_on_submit():
            # Save or update unit price
            unit_price = unit_price_form.unit_price.data
            if not system_settings:
                current_app.logger.info('Creating new system settings')
                system_settings = Settings(unit_price=unit_price)
                db.session.add(system_settings)
            else:
                current_app.logger.info('Updating unit price')
                system_settings.unit_price = unit_price
            flash('Unit price updated successfully!', 'success')
            db.session.commit()
            return redirect(url_for('accounts.settings.settings'))

        elif 'add_section_submit' in request.form and add_section_form.validate_on_submit():
            # Add a new house section
            house_section = add_section_form.house_sections.data

            # Logic to add the new house section
            if system_settings:
                existing_sections = system_settings.house_sections.split(',') if system_settings.house_sections else []
                if house_section not in existing_sections:
                    existing_sections.append(house_section)
                    system_settings.house_sections = ','.join(existing_sections)
                    db.session.commit()
                    flash(f'House section "{house_section}" added successfully!', 'success')
            return redirect(url_for('accounts.settings.settings'))

        # Update the existing logic for your route handling
        # ...

        # Inside your route handling logic
        elif 'edit_section_submit' in request.form and edit_section_form.validate_on_submit():
            # Edit the selected house section
            selected_section = edit_section_form.house_sections.data
            new_house_section = edit_section_form.new_house_section.data

            # Logic to update the selected house section
            current_app.logger.info(f'Editing house section: "{selected_section}" to "{new_house_section}"')
            flash(f'House section "{selected_section}" updated to "{new_house_section}" successfully!', 'success')

            # Update the house section in the database
            if system_settings:
                house_sections = system_settings.house_sections.split(',') if system_settings.house_sections else []
                if selected_section in house_sections:
                    house_sections.remove(selected_section)
                    house_sections.append(new_house_section)
                    system_settings.house_sections = ','.join(house_sections)
                    db.session.commit()

            return redirect(url_for('accounts.settings.settings'))

        elif 'delete_section_submit' in request.form and delete_section_form.validate_on_submit():
            # Delete the selected house section
            selected_section = delete_section_form.house_sections.data

            # Logic to delete the selected house section
            current_app.logger.info(f'Deleting house section: "{selected_section}"')

            # Delete the house section in the database
            if system_settings:
                house_sections = system_settings.house_sections.split(',') if system_settings.house_sections else []
                if selected_section in house_sections:
                    house_sections.remove(selected_section)
                    system_settings.house_sections = ','.join(house_sections)
                    db.session.commit()

            flash(f'House section "{selected_section}" deleted successfully!', 'success')
            return redirect(url_for('accounts.settings.settings'))


        flash(f'there was an error!', 'danger')
        return redirect(url_for('accounts.settings.settings'))

    return render_template('accounts/settings.html',
                           unit_price_form=unit_price_form,
                           add_section_form=add_section_form,
                           edit_section_form=edit_section_form,
                           delete_section_form=delete_section_form,
                           hide_footer=True)
