# app/backend/accounts/records/paymrnt_logic.py

from datetime import datetime, timezone, timedelta
from app import db
from ...models.user import Payment

def make_payment_logic(bill_id, meter_reading, payment_amount, payment_method, reference_number, status, user_id, reading_id):
    try:
        # Check if the payment amount is greater than 0
        if payment_amount <= 0:
            return {'success': False, 'message': 'Payment amount must be greater than 0'}

        # Extract the user_id from the meter_reading object
        reading_id = meter_reading.id

        # Create a new Payment object
        payment = Payment(
            bill_id=bill_id,
            amount=payment_amount,
            payment_date=datetime.now(timezone.utc) + timedelta(hours=3),
            payment_method=payment_method,
            reference_number=reference_number,
            status=status,
            user_id=user_id,
            reading_id=reading_id
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
