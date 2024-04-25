# File: app/backend/accounts/records/payment_logic.py

from core import db
from ...database.models import *
from ..components.payment_processor import process_payments_with_context


def make_payment_logic(meter_reading, payment_amount, payment_method, reference_number, status, user_id, invoice_id, invoice_amount):
    try:
        if payment_amount <= 0:
            return {'success': False, 'message': 'Payment amount must be greater than 0'}

        invoice_id = meter_reading.id
        customer_name = meter_reading.customer_name
        invoice_amount = meter_reading.total_amount

        payment = Payment(
            amount=payment_amount,
            timestamp=default_datetime(),
            payment_method=payment_method,
            reference_number=reference_number,
            status=status,
            user_id=user_id,
            invoice_id=invoice_id,
            invoice_amount=invoice_amount,
            customer_name=customer_name
        )
        db.session.add(payment)
        db.session.commit()

        process_payments_with_context()

        return {'success': True, 'message': 'Payment successful'}

    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': f'An error occurred during payment processing: {str(e)}'}


def validate_payment_logic(payment_id):
    try:
        payment = Payment.query.get(payment_id)

        if payment:
            payment.status = not payment.status
            db.session.commit()

            return {'success': True, 'message': 'Payment status updated successfully.'}
        else:
            return {'success': False, 'message': 'Payment not found.'}

    except Exception as e:
        return {'success': False, 'message': f'Error updating payment status: {str(e)}'}


def delete_payment_logic(payment_id):
    try:
        payments = Payment.query.get(payment_id)

        if payments:
            db.session.delete(payments)
            db.session.commit()

            process_payments_with_context()

            return {'success': True, 'message': 'Payment deleted successfully.'}
        else:
            return {'success': False, 'message': 'Payment not found.'}

    except Exception as e:
        return {'success': False, 'message': f'Error deleting payment: {str(e)}'}
