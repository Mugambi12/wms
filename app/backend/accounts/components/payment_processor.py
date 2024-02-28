# File: app/backend/payment_processor.py

from sqlalchemy import func
from app import create_app, db
from ...database.models import User, MeterReading, Payment

def process_payments_with_context():
    app = create_app()
    with app.app_context():
        process_payments()

def process_payments():
    try:
        # Get total payment amount and total meter reading total price for each user
        payment_data = db.session.query(
            Payment.unique_user_id,
            func.sum(Payment.amount).label('total_payment_amount')
        ).group_by(Payment.unique_user_id).all()

        meter_reading_data = db.session.query(
            MeterReading.unique_user_id,
            func.sum(MeterReading.total_price).label('total_meter_reading_total_price')
        ).group_by(MeterReading.unique_user_id).all()

        # Bulk fetch users to update their balances
        user_ids = set([payment.unique_user_id for payment in payment_data])
        user_ids.update([meter_reading.unique_user_id for meter_reading in meter_reading_data])
        users = User.query.filter(User.unique_user_id.in_(user_ids)).all()
        user_mapping = {user.unique_user_id: user for user in users}

        # Update user balances
        update_user_balances(payment_data, meter_reading_data, user_mapping)

        # Update MeterReading statuses
        update_meter_reading_statuses(meter_reading_data)

        # Commit changes to the database
        db.session.commit()

    except Exception as e:
        print(f"An error occurred while processing payments: {e}")
        db.session.rollback()

def update_user_balances(payment_data, meter_reading_data, user_mapping):
    for payment, meter_reading in zip(payment_data, meter_reading_data):
        user_id = payment.unique_user_id
        total_payment_amount = payment.total_payment_amount or 0
        total_meter_reading_total_price = meter_reading.total_meter_reading_total_price or 0
        balance_difference = total_payment_amount - total_meter_reading_total_price

        # Update user balance
        if user_id in user_mapping:
            user_mapping[user_id].balance = balance_difference
        else:
            # If the user doesn't exist, create a new user entry with the calculated balance
            new_user = User(unique_user_id=user_id, balance=balance_difference)
            db.session.add(new_user)

def update_meter_reading_statuses():
    all_meter_readings = MeterReading.query.all()

    for meter_reading in all_meter_readings:
        user_id = meter_reading.unique_user_id
        all_payments_by_a_user = Payment.query.filter_by(unique_user_id=user_id).all()
        meter_readings = MeterReading.query.filter_by(unique_user_id=user_id).order_by(MeterReading.id).all()

        total_payments_so_far = sum(payment.amount for payment in all_payments_by_a_user)
        total_price_so_far = meter_reading.total_meter_reading_total_price or 0

        for reading in meter_readings:
            total_price_so_far += reading.total_price

            if total_price_so_far > total_payments_so_far:
                for reading_to_update in meter_readings:
                    reading_to_update.reading_status = True
                break
            else:
                reading.reading_status = False
