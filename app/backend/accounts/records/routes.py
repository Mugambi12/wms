# app/backend/accounts/records/routes.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from .forms import AddMeterReadingForm, EditMeterReadingForm
from ...models.user import MeterReading, User

records_bp = Blueprint('records', __name__, url_prefix='/records')

@records_bp.route('/meter_readings', methods=['GET', 'POST'])
@login_required
def meter_readings():
    form = AddMeterReadingForm()

    house_sections = db.session.query(User.house_section).distinct().all()

    meter_readings = MeterReading.query.filter_by(user_id=current_user.id).all()

    if form.validate_on_submit():
        reading_value = form.reading_value.data
        house_section = form.house_section.data
        house_number = form.house_number.data

        if not User.query.filter_by(house_section=house_section).first():
            flash('The selected house section is not registered.', 'danger')
        elif not User.query.filter_by(house_number=house_number).first():
            flash('The entered house number is not registered.', 'danger')
        elif not User.query.filter_by(house_section=house_section, house_number=house_number).first():
            flash('The combination of house section and house number does not match.', 'danger')
        else:
            try:
                new_meter_reading = MeterReading(
                    reading_value=reading_value,
                    house_section=house_section,
                    house_number=house_number,
                    user_id=current_user.id
                )
                db.session.add(new_meter_reading)
                db.session.commit()

                flash('Meter reading added successfully!', 'success')

                return redirect(url_for('accounts.records.meter_readings'))

            except Exception as e:
                flash(f'Error adding meter reading: {str(e)}', 'danger')
#    else:
#        flash('Please check your input values. The form is not valid.', 'warning')

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
