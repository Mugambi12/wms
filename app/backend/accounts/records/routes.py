# app/backend/accounts/records/routes.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from .forms import AddMeterReadingForm, EditMeterReadingForm
from ...models.user import MeterReading, User, Settings

records_bp = Blueprint('records', __name__, url_prefix='/records')

@records_bp.route('/meter_readings', methods=['GET', 'POST'])
@login_required
def meter_readings():
    form = AddMeterReadingForm()
    edit_form = AddMeterReadingForm()
    if request.method == 'POST':
        # Handle form submissions for adding, editing, and deleting
        form_type = request.form.get('form_type')

        if form_type == 'add':
            return handle_add_meter_reading()

        elif form_type == 'edit':
            return handle_edit_meter_reading()

        elif form_type == 'delete':
            return handle_delete_meter_reading()

    # Fetch data needed for rendering the main page
    house_sections = db.session.query(User.house_section.distinct()).all()
    meter_readings = MeterReading.query.filter_by(user_id=current_user.id).all()

    return render_template('accounts/meter_readings.html', form=form, edit_form=edit_form, house_sections=house_sections, meter_readings=meter_readings, hide_footer=True)


def handle_add_meter_reading():
    try:
        form = AddMeterReadingForm(request.form)
        if form.validate_on_submit():
            # Create a new MeterReading instance
            new_reading = MeterReading(
                house_section=form.house_section.data,
                house_number=form.house_number.data,
                reading_value=form.reading_value.data,
                user_id=current_user.id
            )

            # Add and commit the new meter reading to the database
            db.session.add(new_reading)
            db.session.commit()

            flash('Meter reading added successfully!', 'success')
        else:
            flash('Invalid form submission for adding meter reading.', 'danger')

    except Exception as e:
        flash(f'Error adding meter reading: {str(e)}', 'danger')

    return redirect(url_for('accounts.records.meter_readings'))


def handle_edit_meter_reading():
    try:
        form = EditMeterReadingForm(request.form)
        if form.validate_on_submit():
            # Retrieve the meter reading to be edited
            meter_reading_id = request.form.get('meter_reading_id')
            edited_reading = MeterReading.query.get_or_404(meter_reading_id)

            # Update the meter reading attributes
            edited_reading.house_section = form.house_section.data
            edited_reading.house_number = form.house_number.data
            edited_reading.reading_value = form.reading_value.data
            edited_reading.timestamp = form.timestamp.data
            edited_reading.reading_status = form.reading_status.data

            # Commit the changes to the database
            db.session.commit()

            flash('Meter reading updated successfully!', 'success')
        else:
            flash('Invalid form submission for editing meter reading.', 'danger')

    except Exception as e:
        flash(f'Error updating meter reading: {str(e)}', 'danger')

    return redirect(url_for('accounts.records.meter_readings'))


def handle_delete_meter_reading():
    try:
        # Retrieve the meter reading to be deleted
        meter_reading_id = request.form.get('meter_reading_id')
        deleted_reading = MeterReading.query.get_or_404(meter_reading_id)

        # Delete the meter reading from the database
        db.session.delete(deleted_reading)
        db.session.commit()

        flash('Meter reading deleted successfully!', 'success')

    except Exception as e:
        flash(f'Error deleting meter reading: {str(e)}', 'danger')

    return redirect(url_for('accounts.records.meter_readings'))















@records_bp.route('/billing')
@login_required
def billing():
    if current_user.is_authenticated:
        billing_data = (
            db.session.query(
                MeterReading.id,
                MeterReading.timestamp,
                User.first_name,
                User.last_name,
                MeterReading.house_section,
                MeterReading.house_number,
                User.is_active,
                MeterReading.reading_value.label('prev_reading'),
                MeterReading.reading_value.label('curr_reading'),
                MeterReading.consumed,
                MeterReading.unit_price,
                MeterReading.total_price
            )
            .join(User)
            .filter(User.id == current_user.id)
            .order_by(MeterReading.timestamp.desc())
            .all()
        )

        return render_template('accounts/billing.html', hide_footer=True, billing_data=billing_data)
    else:
        return redirect(url_for('auth.login'))






@records_bp.route('/invoice')
@login_required
def invoice():
    # Check if the user is still authenticated
    if current_user.is_authenticated:
        # You can add records-specific logic and data here
        return render_template('accounts/invoice.html', hide_sidebar=True, hide_navbar=True, hide_footer=True)
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
