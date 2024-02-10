# app/backend/accounts/records/meter_readings.py
from flask import request, flash
from sqlalchemy.exc import SQLAlchemyError
from app import db
from ...models.user import MeterReading, User, Settings
from .forms import MakePaymentForm


def make_payment_logic(edited_reading):
    make_payment_form = MakePaymentForm(
        customer_name=edited_reading.customer_name,
        house_section=edited_reading.house_section,
        house_number=edited_reading.house_number,
        reading_value=edited_reading.reading_value,
        consumed=edited_reading.consumed,
        unit_price=edited_reading.unit_price,
        total_price=edited_reading.total_price,
        timestamp=edited_reading.timestamp,
        reading_status=edited_reading.reading_status
    )

    if request.method == 'POST':
        try:
            # Update the form with the submitted data
            if make_payment_form.validate_on_submit():
                edited_reading.customer_name = make_payment_form.customer_name.data
                edited_reading.house_section = make_payment_form.house_section.data
                edited_reading.house_number = make_payment_form.house_number.data
                edited_reading.reading_value = make_payment_form.reading_value.data
                edited_reading.timestamp = make_payment_form.timestamp.data
                edited_reading.consumed = make_payment_form.consumed.data
                edited_reading.unit_price = make_payment_form.unit_price.data
                edited_reading.total_price = make_payment_form.total_price.data
                edited_reading.reading_status = make_payment_form.reading_status.data

                db.session.commit()

                return {'success': True, 'message': 'Meter reading updated successfully!', 'form': None}

            else:
                flash('Invalid form submission for editing meter reading.', 'danger')

        except Exception as e:
            flash(f'Error updating meter reading: {str(e)}', 'danger')

    return {'success': False, 'message': 'Error updating meter reading.', 'form': make_payment_form}
