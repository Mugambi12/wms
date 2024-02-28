from sqlalchemy import func, and_
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

from collections import defaultdict

def update_user_balances(payment_data, meter_reading_data, user_mapping):
    # Create a dictionary to group users by house section and house number
    grouped_users = defaultdict(list)
    for user_id, user in user_mapping.items():
        grouped_users[(user.house_section, user.house_number)].append(user)

    # Update balances for users in each group
    for users_group in grouped_users.values():
        total_payment_amount = 0
        total_meter_reading_total_price = 0

        # Calculate total payment amount and total meter reading total price for the group
        for user in users_group:
            payment = next((payment for payment in payment_data if payment.unique_user_id == user.unique_user_id), None)
            meter_reading = next((reading for reading in meter_reading_data if reading.unique_user_id == user.unique_user_id), None)
            if payment:
                total_payment_amount += payment.total_payment_amount or 0
            if meter_reading:
                total_meter_reading_total_price += meter_reading.total_meter_reading_total_price or 0

        # Calculate balance difference for the group
        balance_difference = total_payment_amount - total_meter_reading_total_price

        # Update balances for users in the group
        for user in users_group:
            user.balance = balance_difference

            # If the user is not in the user_mapping, add it to the session
            if user.unique_user_id not in user_mapping:
                db.session.add(user)


def update_meter_reading_statuses(meter_reading_data):
    for meter_reading in meter_reading_data:
        user_id = meter_reading.unique_user_id
        all_payments_by_a_user = Payment.query.filter_by(unique_user_id=user_id).all()
        meter_readings = MeterReading.query.filter_by(unique_user_id=user_id).order_by(MeterReading.id).all()
        total_payments_so_far = sum(payment.amount for payment in all_payments_by_a_user)

        total_price_so_far = meter_reading.total_meter_reading_total_price or 0
        total_price_so_far = 0

        for reading in meter_readings:
            total_price_so_far += reading.total_price

            if total_price_so_far > total_payments_so_far:
                for reading_to_update in meter_readings:
                    reading_to_update.reading_status = False
                break
            else:
                reading.reading_status = True
