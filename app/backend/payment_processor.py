from sqlalchemy import func, and_
from app import create_app, db
from .database.models import User, MeterReading, Payment

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

        # Update user balances and reading/payment status
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

        # Bulk update MeterReading and Payment statuses
        meter_reading_ids = set([meter_reading.unique_user_id for meter_reading in meter_reading_data])
        payments = Payment.query.filter(and_(Payment.unique_user_id.in_(meter_reading_ids), Payment.status==False)).all()
        meter_readings = MeterReading.query.filter(MeterReading.unique_user_id.in_(meter_reading_ids)).order_by(MeterReading.unique_user_id, MeterReading.id).all()
        total_payment_amount_so_far = {user_id: 0 for user_id in meter_reading_ids}
        for reading in meter_readings:
            user_id = reading.unique_user_id
            total_payment_amount_so_far[user_id] += reading.total_price
            if total_payment_amount_so_far[user_id] >= total_payment_amount:
                reading.reading_status = False
            else:
                reading.reading_status = True

        for payment in payments:
            user_id = payment.unique_user_id
            total_meter_reading_price = 0
            for reading in meter_readings:
                if reading.unique_user_id == user_id:
                    total_meter_reading_price += reading.total_price
            if total_payment_amount_so_far[user_id] >= total_meter_reading_price:
                payment.status = True
            else:
                payment.status = False

        # Commit changes to the database
        db.session.commit()

    except Exception as e:
        print(f"An error occurred while processing payments: {e}")
        db.session.rollback()
