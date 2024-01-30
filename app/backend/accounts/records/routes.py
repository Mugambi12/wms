# app/backend/accounts/records/routes.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from .forms import AddMeterReadingForm
from ...models.user import MeterReading

records_bp = Blueprint('records', __name__, url_prefix='/records')

@records_bp.route('/meter_readings', methods=['GET', 'POST'])
@login_required
def meter_readings():
    form = AddMeterReadingForm()

    if form.validate_on_submit():
        reading_value = form.reading_value.data
        reading_date = form.reading_date.data
        house_section = form.house_section.data
        house_number = form.house_number.data

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

            flash('Meter reading added successfully!', 'success')
            return redirect(url_for('accounts.records.meter_readings'))

        except Exception as e:
            # Handle any exceptions, e.g., validation errors
            flash(f'Error adding meter reading: {str(e)}', 'error')

    return render_template('accounts/meter_readings.html', form=form, hide_footer=True)


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
