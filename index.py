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

    # Fetch distinct house sections from the database
    house_sections = db.session.query(User.house_section).distinct().all()

    # Fetch meter readings for the current user
    meter_readings = MeterReading.query.filter_by(user_id=current_user.id).all()

    if form.validate_on_submit():
        house_section = form.house_section.data
        house_number = form.house_number.data
        reading_value = form.reading_value.data

        # Check if the house section and house number are valid
        user = User.query.filter_by(house_section=house_section, house_number=house_number).first()
        if not user:
            flash('Invalid house section or house number.', 'danger')
        else:
            try:
                # Fetch the latest meter reading for the specified house section and number
                latest_reading = MeterReading.query.filter_by(
                    house_section=house_section, house_number=house_number
                ).order_by(MeterReading.timestamp.desc()).first()

                # Calculate consumed and total_price based on the latest meter reading
                old_prev_reading = 0 if latest_reading is None else latest_reading.reading_value
                consumed = reading_value - old_prev_reading

                # Fetch unit_price from the Settings model
                unit_price_row = db.session.query(Settings.unit_price).first()
                unit_price = 0 if not unit_price_row else unit_price_row[0]
                total_price = consumed * unit_price

                # Create a new MeterReading instance
                new_meter_reading = MeterReading(
                    reading_value=reading_value,
                    house_section=house_section,
                    house_number=house_number,
                    user_id=current_user.id,
                    consumed=consumed,
                    unit_price=unit_price,
                    total_price=total_price
                )

                # Add and commit the new meter reading to the database
                db.session.add(new_meter_reading)
                db.session.commit()

                flash('Meter reading added successfully!', 'success')
                return redirect(url_for('accounts.records.meter_readings'))

            except Exception as e:
                flash(f'Error adding meter reading: {str(e)}', 'danger')

    return render_template('accounts/meter_readings.html', form=form, house_sections=house_sections, meter_readings=meter_readings, hide_footer=True)


@records_bp.route('/edit_meter_reading/<int:meter_reading_id>', methods=['GET', 'POST'])
@login_required
def edit_meter_reading(meter_reading_id):
    meter_reading = MeterReading.query.get_or_404(meter_reading_id)

    if meter_reading.user_id != current_user.id:
        flash('You do not have permission to edit this meter reading.', 'danger')
        return redirect(url_for('accounts.records.meter_readings'))

    form = EditMeterReadingForm(obj=meter_reading)

    if form.validate_on_submit():
        try:
            # Update the meter reading attributes
            form.populate_obj(meter_reading)
            db.session.commit()

            flash('Meter reading updated successfully!', 'success')

            return redirect(url_for('accounts.records.meter_readings'))

        except Exception as e:
            flash(f'Error updating meter reading: {str(e)}', 'danger')

    return render_template('accounts/edit_records.html', form=form, meter_reading=meter_reading, hide_footer=True)


@records_bp.route('/delete_meter_reading/<int:meter_reading_id>', methods=['POST'])
@login_required
def delete_meter_reading(meter_reading_id):
    meter_reading = MeterReading.query.get_or_404(meter_reading_id)

    if meter_reading.user_id != current_user.id:
        flash('You do not have permission to delete this meter reading.', 'danger')
        return redirect(url_for('accounts.records.meter_readings'))

    try:
        db.session.delete(meter_reading)
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
