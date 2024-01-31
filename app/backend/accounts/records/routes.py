# app/backend/accounts/records/routes.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from .forms import AddMeterReadingForm
from ...models.user import MeterReading, User

records_bp = Blueprint('records', __name__, url_prefix='/records')

@records_bp.route('/meter_readings', methods=['GET', 'POST'])
@login_required
def meter_readings():
    # Create an instance of the AddMeterReadingForm
    form = AddMeterReadingForm()

    # Query available house sections from registered users
    house_sections = db.session.query(User.house_section).distinct().all()

    # Query all meter readings for the current user
    meter_readings = MeterReading.query.filter_by(user_id=current_user.id).all()

    # Check if the form is submitted and valid
    if form.validate_on_submit():
        # Extract data from the form
        reading_value = form.reading_value.data
        reading_date = form.reading_date.data
        house_section = form.house_section.data
        house_number = form.house_number.data

        # Check if the entered house number is registered in the User model
        if not User.query.filter_by(house_section=house_section).first():
            flash('House section is not registered. Please enter a valid house section.', 'danger')
        elif not User.query.filter_by(house_number=house_number).first():
            flash('House number is not registered. Please enter a valid house number.', 'danger')
        elif not User.query.filter_by(house_section=house_section, house_number=house_number).first():
            flash('House section and House number do not match. Please enter a valid combination.', 'danger')
        else:
            try:
                # Create a new MeterReading object and add it to the database
                new_meter_reading = MeterReading(
                    reading_value=reading_value,
                    reading_date=reading_date,
                    house_section=house_section,
                    house_number=house_number,
                    user_id=current_user.id
                )
                db.session.add(new_meter_reading)
                db.session.commit()

                # Flash a success message
                flash('Meter reading added successfully!', 'success')

                # Redirect to the meter_readings route to display the updated list
                return redirect(url_for('accounts.records.meter_readings'))

            except Exception as e:
                # Handle any exceptions, e.g., validation errors or database issues
                flash(f'Error adding meter reading: {str(e)}', 'error')

    # Render the template with the form, available house sections, and meter readings
    return render_template('accounts/meter_readings.html', form=form, house_sections=house_sections, meter_readings=meter_readings, hide_footer=True)






@records_bp.route('/billing')
@login_required
def billing():
    # Check if the user is still authenticated
    if current_user.is_authenticated:
        # You can add records-specific logic and data here
        return render_template('accounts/billing.html', hide_footer=True)
    else:
        # If the user is not authenticated, redirect to the login page
        return redirect(url_for('auth.login'))

@records_bp.route('/payments')
@login_required
def payments():
    # Check if the user is still authenticated
    if current_user.is_authenticated:
        # You can add records-specific logic and data here
        return render_template('accounts/payments.html', hide_footer=True)
    else:
        # If the user is not authenticated, redirect to the login page
        return redirect(url_for('auth.login'))
