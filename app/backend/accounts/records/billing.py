# app/backend/accounts/records/billing.py
from flask_login import current_user
from app import db
from ...models.user import MeterReading, User, Payment

from sqlalchemy import func

def fetch_billing_data():
    get_billing_data = (
            db.session.query(
                MeterReading.id,
                MeterReading.timestamp,
                MeterReading.house_section,
                MeterReading.house_number,
                MeterReading.reading_status,
                MeterReading.customer_name,
                func.lag(MeterReading.reading_value)
                .over(partition_by=(MeterReading.house_section, MeterReading.house_number), order_by=MeterReading.timestamp)
                .label('prev_reading'),
                MeterReading.reading_value.label('curr_reading'),
                MeterReading.consumed,
                MeterReading.unit_price,
                MeterReading.sub_total_price,
                MeterReading.service_fee,
                MeterReading.total_price
            )
            .join(User)
            .filter(User.id == current_user.id)
            .order_by(MeterReading.timestamp.desc())
            .all()
        )
    return get_billing_data


def fetch_invoice_data(invoice_id):
    invoice = MeterReading.query.filter_by(id=invoice_id).first()
    if invoice:
        user = User.query.filter_by(id=invoice.user_id).first()

        service_qty = (
            MeterReading.query
            .filter(
                MeterReading.house_section == invoice.house_section,
                MeterReading.house_number == invoice.house_number,
                MeterReading.reading_status == False
            )
            .group_by(MeterReading.house_section, MeterReading.house_number)
            .count()
        )

        if user:
            invoice_data = {
                'mobile': user.mobile_number,
                'first_service': 'Water Usage',
                'first_description': 'Monthly water consumption',
                'second_service': 'Service Fee',
                'second_description': 'Maintenance & service charge',
                'invoice_id': invoice.id,
                'timestamp': invoice.timestamp,
                'customer_name': invoice.customer_name,
                'house_section': invoice.house_section,
                'house_number': invoice.house_number,
                'reading_value': invoice.reading_value,
                'unit_price': invoice.unit_price,
                'service_fee': invoice.service_fee,
                'consumed': invoice.consumed,
                'service_qty': service_qty,
                'sub_total_price': invoice.sub_total_price,
                'total_price': invoice.total_price,
                'reading_status': invoice.reading_status,
                'vat': '0'
            }
            return invoice_data
        else:
            return None
    else:
        return None


def fetch_payment_data():
    try:
        # Fetch all payment records from the database
        payments = Payment.query.all()

        # Initialize an empty list to store payment data
        payment_data = []

        # Iterate over each payment record
        for payment in payments:
            # Create a dictionary to store payment details, including user_id, invoice_id and unique_user_id
            payment_details = {
                'id': payment.id,
                'user_id': payment.user_id,
                'invoice_id': payment.invoice_id,
                'invoice_amount': payment.invoice_amount,
                'amount': payment.amount,
                'payment_date': payment.payment_date,
                'payment_method': payment.payment_method,
                'reference_number': payment.reference_number,
                'status': payment.status
            }
            # Append payment details to the payment_data list
            payment_data.append(payment_details)

        return payment_data

    except Exception as e:
        # Handle any exceptions and return None
        print(f"An error occurred while fetching payment data: {e}")
        return None
