# File: app/backend/accounts/records/meter_readings.py

from flask import request, flash
from sqlalchemy.exc import SQLAlchemyError
from core import db
from ...database.models import MeterReading, User, ServicesSetting
from .forms import EditMeterReadingForm
from ..components.payment_processor import process_payments_with_context


def handle_add_meter_reading(form, current_user):
    try:
        house_section = form.house_section.data
        house_number = form.house_number.data
        reading_value = form.reading_value.data

        if not current_user.is_admin:
            if current_user.house_section != house_section or current_user.house_number != house_number:
                return {'success': False, 'message': 'You are not authorized to add readings for this house.'}

        user = User.query.filter_by(house_section=house_section, house_number=house_number).first()
        if not user:
            return {'success': False, 'message': 'Invalid house section or house number.'}

        latest_reading = MeterReading.query.filter_by(
            house_section=house_section, house_number=house_number
        ).order_by(MeterReading.reading_value.desc()).first()

        old_prev_reading = 0 if latest_reading is None else latest_reading.reading_value

        if old_prev_reading > reading_value:
            return {'success': False, 'message': 'Current reading cannot be less than previous reading.'}

        consumed = reading_value - old_prev_reading

        unit_price = db.session.query(ServicesSetting.unit_price).scalar() or 0
        service_fee = db.session.query(ServicesSetting.service_fee).scalar() or 0

        sub_total_amount = consumed * unit_price
        total_amount = sub_total_amount + service_fee

        customer = f"{user.first_name} {user.last_name}" if user else None

        new_meter_reading = MeterReading(
            reading_value=reading_value,
            house_section=house_section,
            house_number=house_number,
            user_id=user.id,
            customer_name=customer,
            consumed=consumed,
            unit_price=unit_price,
            service_fee=service_fee,
            sub_total_amount=sub_total_amount,
            total_amount=total_amount
        )

        db.session.add(new_meter_reading)
        db.session.commit()

        process_payments_with_context()

        return {'success': True, 'message': 'Meter reading added successfully!'}

    except SQLAlchemyError as e:
        db.session.rollback()
        return {'success': False, 'message': f'Database error: {str(e)}'}
    except ValueError as e:
        return {'success': False, 'message': f'Invalid input: {str(e)}'}
    except Exception as e:
        return {'success': False, 'message': f'Error: {str(e)}'}


def get_meter_readings(current_user):
    query_meter_reading_data = MeterReading.query

    if not current_user.is_admin:
        query_meter_reading_data = query_meter_reading_data.filter(
            MeterReading.house_section == current_user.house_section,
            MeterReading.house_number == current_user.house_number
        )

    meter_reading_data = query_meter_reading_data.all()
    return meter_reading_data


def edit_meter_reading_logic(edited_reading):
    edit_meter_reading_form = EditMeterReadingForm(
        customer_name=edited_reading.customer_name,
        house_section=edited_reading.house_section,
        house_number=edited_reading.house_number,
        reading_value=edited_reading.reading_value,
        consumed=edited_reading.consumed,
        unit_price=edited_reading.unit_price,
        total_amount=edited_reading.total_amount,
        timestamp=edited_reading.timestamp
    )

    if request.method == 'POST':
        try:
            if edit_meter_reading_form.validate_on_submit():
                edited_reading.customer_name = edit_meter_reading_form.customer_name.data
                edited_reading.house_section = edit_meter_reading_form.house_section.data
                edited_reading.house_number = edit_meter_reading_form.house_number.data
                edited_reading.reading_value = edit_meter_reading_form.reading_value.data
                edited_reading.timestamp = edit_meter_reading_form.timestamp.data
                edited_reading.consumed = edit_meter_reading_form.consumed.data
                edited_reading.unit_price = edit_meter_reading_form.unit_price.data
                edited_reading.total_amount = edit_meter_reading_form.total_amount.data

                db.session.commit()

                process_payments_with_context()

                return {'success': True, 'message': 'Meter reading updated successfully!', 'form': None}

            else:
                flash('Invalid form submission for editing meter reading.', 'danger')

        except Exception as e:
            flash(f'Error updating meter reading: {str(e)}', 'danger')

    return {'success': False, 'message': 'Error updating meter reading.', 'form': edit_meter_reading_form}


def delete_meter_reading_logic(meter_reading_id):
    try:
        meter_reading = MeterReading.query.get(meter_reading_id)

        if meter_reading:
            db.session.delete(meter_reading)
            db.session.commit()

            process_payments_with_context()

            return {'success': True, 'message': 'Meter reading deleted successfully.'}
        else:
            return {'success': False, 'message': 'Meter reading not found.'}

    except Exception as e:
        return {'success': False, 'message': f'Error deleting meter reading: {str(e)}'}
