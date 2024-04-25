from sqlalchemy import func
from collections import defaultdict
from core import create_app, db
from ...database.models import User, MeterReading, Payment


def process_payments_with_context():
    app = create_app()
    with app.app_context():
        process_payments()


def process_payments():
    try:
        payment_data = db.session.query(
            Payment.user_id,
            func.sum(Payment.amount).label('total_payment_amount')
        ).group_by(Payment.user_id).all()

        meter_reading_data = db.session.query(
            MeterReading.user_id,
            func.sum(MeterReading.total_amount).label('total_meter_reading_total_amount')
        ).group_by(MeterReading.user_id).all()

        user_ids = set([payment.user_id for payment in payment_data])
        user_ids.update([meter_reading.user_id for meter_reading in meter_reading_data])
        users = User.query.filter(User.id.in_(user_ids)).all()
        user_mapping = {user.id: user for user in users}

        update_user_balances(payment_data, meter_reading_data, user_mapping)

        update_meter_payment_statuses(meter_reading_data, payment_data)

        db.session.commit()

    except Exception as e:
        print(f"An error occurred while processing payments: {e}")
        db.session.rollback()


def update_user_balances(payment_data, meter_reading_data, user_mapping):
    grouped_users = defaultdict(list)
    for user_id, user in user_mapping.items():
        grouped_users[(user.house_section, user.house_number)].append(user)

    for users_group in grouped_users.values():
        total_payment_amount = 0
        total_meter_reading_total_amount = 0

        for user in users_group:
            payment = next((payment for payment in payment_data if payment.user_id == user.id), None)
            meter_reading = next((reading for reading in meter_reading_data if reading.user_id == user.id), None)
            if payment:
                total_payment_amount += payment.total_payment_amount or 0
            if meter_reading:
                total_meter_reading_total_amount += meter_reading.total_meter_reading_total_amount or 0

        balance_difference = total_payment_amount - total_meter_reading_total_amount

        for user in users_group:
            user.balance = balance_difference

            if user.id not in user_mapping:
                db.session.add(user)


def update_meter_payment_statuses(meter_reading_data, payment_data):
    for meter_reading in meter_reading_data:
        user_id = meter_reading.user_id
        total_meter_reading_total_amount = meter_reading.total_meter_reading_total_amount or 0

        all_payments_by_a_user = [payment for payment in payment_data if payment.user_id == user_id]

        total_payments_so_far = sum(payment.total_payment_amount for payment in all_payments_by_a_user)

        meter_readings = MeterReading.query.filter_by(user_id=user_id).order_by(MeterReading.id).all()

        total_amount_so_far = 0

        for reading in meter_readings:
            total_amount_so_far += reading.total_amount

            if total_amount_so_far > total_payments_so_far:
                for reading_to_update in meter_readings[meter_readings.index(reading):]:
                    reading_to_update.payment_status = False
                break
            else:
                reading.payment_status = True
