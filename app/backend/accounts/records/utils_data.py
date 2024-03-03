# File: app/backend/accounts/records/billing.py

from sqlalchemy import func
from flask_login import current_user
from app import db
from ...database.models import MeterReading, User, Payment


def fetch_billing_data(current_user):
    query_billing_data = (
        db.session.query(
            MeterReading.id,
            MeterReading.timestamp,
            MeterReading.house_section,
            MeterReading.house_number,
            MeterReading.payment_status,
            MeterReading.customer_name,
            func.lag(MeterReading.reading_value)
            .over(partition_by=(MeterReading.house_section, MeterReading.house_number), order_by=MeterReading.timestamp)
            .label('prev_reading'),
            MeterReading.reading_value.label('curr_reading'),
            MeterReading.consumed,
            MeterReading.unit_price,
            MeterReading.sub_total_amount,
            MeterReading.service_fee,
            MeterReading.total_amount,
            MeterReading.unique_user_id
        )
        .join(User)
        .order_by(MeterReading.id.desc())
    )

    # If the user is not an admin, filter by their house section and house number
    if not current_user.is_admin:
        query_billing_data = query_billing_data.filter(
            MeterReading.house_section == current_user.house_section,
            MeterReading.house_number == current_user.house_number
        )

    billing_data = query_billing_data.all()

    return billing_data


def fetch_payment_data(current_user):
    try:
        # Construct the query to fetch payment data
        query_payment_data = (
            db.session.query(
                Payment.id,
                Payment.user_id,
                Payment.customer_name,
                Payment.invoice_id,
                Payment.invoice_amount,
                Payment.amount,
                Payment.timestamp,
                Payment.payment_method,
                Payment.reference_number,
                Payment.status,
                Payment.unique_user_id
            )
            .join(User)  # Join Payment table with User table
            .order_by(Payment.timestamp.desc())  # Order by payment date in descending order
        )

        # Filter the payment data based on user role
        if not current_user.is_admin:  # If the current user is not an admin
            query_payment_data = query_payment_data.filter(User.id == current_user.id)  # Filter by user ID
            query_payment_data = query_payment_data.filter(
                User.house_section == current_user.house_section,
                User.house_number == current_user.house_number
            )

        # Execute the query and fetch payment data
        payment_data = query_payment_data.all()  # Fetch all payment data

        return payment_data

    except Exception as e:
        # Handle any exceptions and return None
        print(f"An error occurred while fetching payment data: {e}")
        return None


def fetch_invoice_data(current_user, invoice_id):
    invoice = MeterReading.query.filter_by(id=invoice_id).first()
    if invoice:
        # Check if the current user is an admin
        if current_user.is_admin:
            user = User.query.filter_by(id=invoice.user_id).first()
        else:
            # If the current user is not an admin, filter invoices by the user's house section and house number
            user = User.query.filter_by(id=current_user.id).first()

        service_qty = (
            MeterReading.query
            .filter(
                MeterReading.house_section == invoice.house_section,
                MeterReading.house_number == invoice.house_number,
                MeterReading.payment_status == False
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
                'sub_total_amount': invoice.sub_total_amount,
                'total_amount': invoice.total_amount,
                'payment_status': invoice.payment_status,
                'vat': '0',
                'unique_user_id': invoice.unique_user_id
            }
            return invoice_data
        else:
            return None
    else:
        return None
