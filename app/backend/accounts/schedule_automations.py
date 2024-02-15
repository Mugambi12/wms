from datetime import datetime
from app import db
from ..models.user import MeterReading, Payment

# def process_payments():
#     try:
#         # Retrieve all unpaid meter readings
#         unpaid_meter_readings = MeterReading.query.filter_by(reading_status=False).all()
#
#         for meter_reading in unpaid_meter_readings:
#             # Retrieve all payments for the current meter reading
#             payments = Payment.query.filter_by(invoice_id=meter_reading.id).all()
#
#             # Calculate the total paid amount for the meter reading
#             total_paid_amount = sum(payment.amount for payment in payments)
#
#             # Update meter reading status based on paid amount
#             if total_paid_amount >= meter_reading.total_price:
#                 meter_reading.reading_status = True  # Mark meter reading as paid
#             elif total_paid_amount > 0:
#                 meter_reading.reading_status = False  # Mark meter reading as partially paid
#             else:
#                 meter_reading.reading_status = False  # Mark meter reading as pending
#
#             # Calculate extra amount if paid amount exceeds invoice amount
#             extra_amount = total_paid_amount - meter_reading.total_price
#
#             if extra_amount > 0:
#                 # Roll over extra amount to the next meter reading
#                 next_meter_reading = MeterReading.query.filter(MeterReading.id > meter_reading.id, # MeterReading.reading_status == False).order_by(MeterReading.id).first()
#
#                 if next_meter_reading:
#                     # Update the next meter reading with the extra amount
#                     next_meter_reading.total_price += extra_amount
#                     db.session.commit()
#                 else:
#                     # No next meter reading found, create a new one
#                     new_meter_reading = MeterReading(
#                         reading_value=0,  # Set appropriate values for these attributes
#                         consumed=0,       # depending on your requirements
#                         unit_price=0,
#                         service_fee=0,
#                         sub_total_price=0,
#                         total_price=extra_amount,
#                         reading_status=False,
#                         created_at=datetime.utcnow()
#                     )
#                     db.session.add(new_meter_reading)
#                     db.session.commit()
#
#     except Exception as e:
#         print(f"An error occurred while processing payments: {e}")
#
# from flask_apscheduler import APScheduler
#
# schedule = APScheduler()
#
# # Add this line to the __main__ block to schedule the process_payments function
# schedule.add_job(id='process_payments', func=process_payments, trigger='interval', seconds=3)
# schedule.start()
