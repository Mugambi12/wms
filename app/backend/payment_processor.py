from sqlalchemy import func
from app import create_app, db
from .models.user import User, MeterReading, Payment

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

        # Update user balances
        for payment, meter_reading in zip(payment_data, meter_reading_data):
            user_id = payment.unique_user_id
            total_payment_amount = payment.total_payment_amount or 0
            total_meter_reading_total_price = meter_reading.total_meter_reading_total_price or 0
            balance_difference = total_payment_amount - total_meter_reading_total_price

            user = User.query.filter_by(unique_user_id=user_id).first()
            if user:
                user.balance = balance_difference
            else:
                # If the user doesn't exist, create a new user entry with the calculated balance
                new_user = User(unique_user_id=user_id, balance=balance_difference)
                db.session.add(new_user)

        # Commit changes to the database
        db.session.commit()

    except Exception as e:
        print(f"An error occurred while processing payments: {e}")
        db.session.rollback()
