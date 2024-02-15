# File: app/backend/database/models.py

# Import necessary modules
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from datetime import datetime, timedelta, timezone
import uuid


# Define User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    mobile_number = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(120))
    house_section = db.Column(db.String(50))
    house_number = db.Column(db.String(20))
    profile_image = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    balance = db.Column(db.Float, default=0)
    unique_user_id = db.Column(db.String(6), unique=True, nullable=True)

    # Establishing a one-to-many relationship with meter readings and payments
    meter_readings = db.relationship('MeterReading', backref='user', lazy=True)
    payments = db.relationship('Payment', backref='user', lazy=True)

    def generate_unique_user_id(self):
        while True:
            address = str(uuid.uuid4().int)[:6]
            existing_user = User.query.filter_by(unique_user_id=address).first()
            if not existing_user:
                return address

    def __init__(self, mobile_number, password, first_name=None, last_name=None,
                 email=None, house_section=None, house_number=None, profile_image=None):
        self.mobile_number = mobile_number
        self.password_hash = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.house_section = house_section
        self.house_number = house_number
        self.profile_image = profile_image

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Define MeterReading model
class MeterReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc) + timedelta(hours=3), nullable=False)
    customer_name = db.Column(db.String(50))
    house_section = db.Column(db.String(50))
    house_number = db.Column(db.String(20))
    reading_value = db.Column(db.Float)
    consumed = db.Column(db.Float)
    unit_price = db.Column(db.Float)
    service_fee = db.Column(db.Float)
    sub_total_price = db.Column(db.Float)
    total_price = db.Column(db.Float)
    reading_status = db.Column(db.Boolean, default=False)
    unique_user_id = db.Column(db.String(6))

    # Specify foreign keys explicitly
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Establishing a one-to-many relationship with payments
    payments = db.relationship('Payment', backref='meter_reading', lazy=True)

    def __init__(self, reading_value, house_section, house_number, user_id, unit_price, service_fee, customer_name, consumed, sub_total_price, total_price, unique_user_id=None):
        self.house_section = house_section
        self.house_number = house_number
        self.reading_value = reading_value
        self.user_id = user_id
        self.customer_name = customer_name
        self.consumed = consumed
        self.unit_price = unit_price
        self.service_fee = service_fee
        self.sub_total_price = sub_total_price
        self.total_price = total_price
        self.unique_user_id = unique_user_id


# Define Payment model
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_amount = db.Column(db.Integer)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    reference_number = db.Column(db.String(50))
    status = db.Column(db.Boolean, default=False)
    unique_user_id = db.Column(db.String(6))

    # Specify foreign keys explicitly
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey('meter_reading.id'), nullable=True)

    def __init__(self, amount, payment_date, payment_method, user_id, reference_number=None, status=False, invoice_id=None, invoice_amount=None, unique_user_id=None):
        self.invoice_amount = invoice_amount
        self.amount = amount
        self.payment_date = payment_date
        self.payment_method = payment_method
        self.reference_number = reference_number
        self.status = status
        self.user_id = user_id
        self.invoice_id = invoice_id
        self.unique_user_id = unique_user_id


# Define Settings model
class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255))
    unit_price = db.Column(db.Float)
    service_fee = db.Column(db.Float)
    house_sections = db.Column(db.String(255))
    bank_name = db.Column(db.String(255))
    paybill = db.Column(db.Integer)
    account_number = db.Column(db.Integer)
    contact_number = db.Column(db.String(20))

    def __init__(self, company_name=None, unit_price=None, service_fee=None, house_sections=None, bank_name=None, paybill=None, account_number=None, contact_number=None):
        self.company_name = company_name
        self.unit_price = unit_price
        self.service_fee = service_fee
        self.house_sections = house_sections
        self.bank_name = bank_name
        self.paybill = paybill
        self.account_number = account_number
        self.contact_number = contact_number
