# File: app/backend/accounts/records/payment_logic.py

from datetime import datetime, timezone, timedelta
from app import db
from ...database.models import MeterReading, Payment

def make_payment_logic(meter_reading, payment_amount, payment_method, reference_number, status, user_id, invoice_id, invoice_amount, unique_user_id):
    try:
        # Check if the payment amount is greater than 0
        if payment_amount <= 0:
            return {'success': False, 'message': 'Payment amount must be greater than 0'}

        # Extract the user_id from the meter_reading object
        invoice_id = meter_reading.id
        invoice_amount = meter_reading.total_price
        unique_user_id = meter_reading.unique_user_id

        # Create a new Payment object
        payment = Payment(
            amount=payment_amount,
            payment_date=datetime.now(timezone.utc) + timedelta(hours=3),
            payment_method=payment_method,
            reference_number=reference_number,
            status=status,
            user_id=user_id,
            invoice_id=invoice_id,
            invoice_amount=invoice_amount,
            unique_user_id=unique_user_id
        )

        # Save the payment to the database
        db.session.add(payment)
        db.session.commit()

        # Update the reading status to paid
        meter_reading.reading_status = True
        db.session.commit()

        return {'success': True, 'message': 'Payment successful'}

    except Exception as e:
        # If an error occurs during payment processing, rollback the session and return an error message
        db.session.rollback()
        return {'success': False, 'message': f'An error occurred during payment processing: {str(e)}'}


def delete_payment_logic(payment_id):
    try:
        payments = Payment.query.get(payment_id)

        if payments:
            db.session.delete(payments)
            db.session.commit()
            return {'success': True, 'message': 'Payment deleted successfully.'}
        else:
            return {'success': False, 'message': 'Payment not found.'}

    except Exception as e:
        return {'success': False, 'message': f'Error deleting payment: {str(e)}'}
