# app/backend/accounts/records/routes.py
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from app import db
from .forms import AddMeterReadingForm, EditMeterReadingForm
from ...models.user import MeterReading, User, Settings

records_bp = Blueprint('records', __name__, url_prefix='/records')

@records_bp.route('/meter_readings', methods=['GET', 'POST'])
@login_required
def meter_readings():
    add_meter_reading_form = AddMeterReadingForm()
    edit_meter_reading_form = EditMeterReadingForm()

    if request.method == 'POST':
        form_type = request.form.get('form_type')

        if form_type == 'add':
            result = handle_add_meter_reading(add_meter_reading_form)

            if result['success']:
                flash(result['message'], 'success')
            else:
                flash(result['message'], 'danger')

        elif form_type == 'edit':
            result = handle_edit_meter_reading(edit_meter_reading_form)

            if result['success']:
                flash(result['message'], 'success')
            else:
                flash(result['message'], 'danger')

        elif form_type == 'delete':
            result = handle_delete_meter_reading()

            if result['success']:
                flash(result['message'], 'success')
            else:
                flash(result['message'], 'danger')

    house_sections = db.session.query(User.house_section.distinct()).all()
    meter_readings = MeterReading.query.filter_by(user_id=current_user.id).all()

    return render_template('accounts/meter_readings.html', house_sections=house_sections, meter_readings=meter_readings, hide_footer=True, form=add_meter_reading_form, edit_form=edit_meter_reading_form)

def handle_add_meter_reading(form):
    house_sections = db.session.query(User.house_section).distinct().all()
    meter_readings = MeterReading.query.filter_by(user_id=current_user.id).all()

    if form.validate_on_submit():
        house_section = form.house_section.data
        house_number = form.house_number.data
        reading_value = form.reading_value.data

        user = User.query.filter_by(house_section=house_section, house_number=house_number).first()

        if not user:
            return {'success': False, 'message': 'Invalid house section or house number.'}
        else:
            try:
                latest_reading = MeterReading.query.filter_by(
                    house_section=house_section, house_number=house_number
                ).order_by(MeterReading.timestamp.desc()).first()

                old_prev_reading = 0 if latest_reading is None else latest_reading.reading_value
                consumed = reading_value - old_prev_reading

                unit_price_row = db.session.query(Settings.unit_price).first()
                unit_price = 0 if not unit_price_row else unit_price_row[0]
                total_price = consumed * unit_price

                new_meter_reading = MeterReading(
                    reading_value=reading_value,
                    house_section=house_section,
                    house_number=house_number,
                    user_id=current_user.id,
                    consumed=consumed,
                    unit_price=unit_price,
                    total_price=total_price
                )

                db.session.add(new_meter_reading)
                db.session.commit()

                return {'success': True, 'message': 'Meter reading added successfully!'}

            except Exception as e:
                return {'success': False, 'message': f'Error adding meter reading: {str(e)}'}
    else:
        return {'success': False, 'message': 'Invalid form submission for adding meter reading.'}



@records_bp.route('/edit_meter_reading/<int:meter_reading_id>', methods=['GET', 'POST'])
@login_required
def edit_meter_reading(meter_reading_id):
    # Fetch the existing meter reading from the database
    edited_reading = MeterReading.query.get_or_404(meter_reading_id)

    # Create an instance of the EditMeterReadingForm and set default values
    edit_meter_reading_form = EditMeterReadingForm(obj=edited_reading)

    if request.method == 'POST':
        try:
            # Update the form with the submitted data
            if edit_meter_reading_form.validate_on_submit():
                edited_reading.house_section = edit_meter_reading_form.house_section.data
                edited_reading.house_number = edit_meter_reading_form.house_number.data
                edited_reading.reading_value = edit_meter_reading_form.reading_value.data
                edited_reading.timestamp = edit_meter_reading_form.timestamp.data
                edited_reading.consumed = edit_meter_reading_form.consumed.data
                edited_reading.unit_price = edit_meter_reading_form.unit_price.data
                edited_reading.total_price = edit_meter_reading_form.total_price.data
                edited_reading.reading_status = edit_meter_reading_form.reading_status.data

                db.session.commit()

                flash('Meter reading updated successfully!', 'success')
                return redirect(url_for('accounts.records.meter_readings'))

            else:
                flash('Invalid form submission for editing meter reading.', 'danger')

        except Exception as e:
            flash(f'Error updating meter reading: {str(e)}', 'danger')

    return render_template('accounts/edit_meter_reading.html', form=edit_meter_reading_form, meter_reading=edited_reading)



@records_bp.route('/delete_meter_reading/<int:meter_reading_id>', methods=['POST'])
@login_required
def delete_meter_reading(meter_reading_id):
    try:
        meter_reading = MeterReading.query.get(meter_reading_id)

        if meter_reading:
            db.session.delete(meter_reading)
            db.session.commit()
            flash('Meter reading deleted successfully.', 'success')
        else:
            flash('Meter reading not found.', 'danger')

        return redirect(url_for('accounts.records.meter_readings'))

    except Exception as e:
        flash(f'Error deleting meter reading: {str(e)}', 'danger')
        return redirect(url_for('accounts.records.meter_readings'))









def handle_edit_meter_reading(form):
    try:
        meter_reading_id = request.form.get('meter_reading_id')
        edited_reading = MeterReading.query.get_or_404(meter_reading_id)

        edited_reading.house_section = form.house_section.data
        edited_reading.house_number = form.house_number.data
        edited_reading.reading_value = form.reading_value.data
        edited_reading.timestamp = form.timestamp.data
        edited_reading.reading_status = form.reading_status.data

        db.session.commit()

        return {'success': True, 'message': 'Meter reading updated successfully!'}

    except Exception as e:
        return {'success': False, 'message': f'Error updating meter reading: {str(e)}'}

def handle_delete_meter_reading():
    try:
        meter_reading_id = request.form.get('meter_reading_id')
        deleted_reading = MeterReading.query.get_or_404(meter_reading_id)

        db.session.delete(deleted_reading)
        db.session.commit()

        return {'success': True, 'message': 'Meter reading deleted successfully!'}

    except Exception as e:
        return {'success': False, 'message': f'Error deleting meter reading: {str(e)}'}













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
