# File: app/backend/accounts/records/billing.py

from sqlalchemy import func
from flask_login import current_user
from core import db
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
            MeterReading.total_amount
        )
        .join(User)
        .order_by(MeterReading.id.desc())
    )

    if not current_user.is_admin:
        query_billing_data = query_billing_data.filter(
            MeterReading.house_section == current_user.house_section,
            MeterReading.house_number == current_user.house_number
        )

    billing_data = query_billing_data.all()

    return billing_data


def fetch_payment_data(current_user):
    try:
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
                Payment.status
            )
            .join(User)
            .order_by(Payment.timestamp.desc())
        )

        if not current_user.is_admin:
            query_payment_data = query_payment_data.filter(User.id == current_user.id)
            query_payment_data = query_payment_data.filter(
                User.house_section == current_user.house_section,
                User.house_number == current_user.house_number
            )

        payment_data = query_payment_data.all()

        return payment_data

    except Exception as e:
        print(f"An error occurred while fetching payment data: {e}")
        return None


def fetch_invoice_data(current_user, invoice_id):
    invoice = MeterReading.query.filter_by(id=invoice_id).first()
    if invoice:
        if current_user.is_admin:
            user = User.query.filter_by(id=invoice.user_id).first()
        else:
            user = User.query.filter_by(id=current_user.id).first()

        service_qty = (
            MeterReading.query
            .filter(
                MeterReading.house_section == invoice.house_section,
                MeterReading.house_number == invoice.house_number,
                MeterReading.payment_status == False
            )
            .group_by(
                MeterReading.id,
                MeterReading.timestamp,
                MeterReading.customer_name,
                MeterReading.house_section,
                MeterReading.house_number,
                MeterReading.reading_value,
                MeterReading.consumed,
                MeterReading.unit_price,
                MeterReading.service_fee,
                MeterReading.sub_total_amount,
                MeterReading.total_amount,
                MeterReading.payment_status,
                MeterReading.user_id
            )
            .count()
        )

        if user:
            invoice_data = {
                'mobile': user.mobile_number,
                'balance': user.balance,
                'first_service': 'Water Usage',
                'first_description': 'Monthly water consumption',
                'second_service': 'Standing Charge',
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
                'vat': '0'
            }
            return invoice_data
        else:
            return None
    else:
        return None

