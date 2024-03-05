# File: app/backend/database/models.py

# Import necessary modules
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import uuid
from app import db


# Function to get the default datetime
def default_datetime():
    return datetime.now(timezone.utc) + timedelta(hours=3)


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

    # New fields for tracking last login and logout
    last_login = db.Column(db.DateTime)
    last_logout = db.Column(db.DateTime)

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


# Define Sticky Notes model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, user_id, content):
        self.user_id = user_id
        self.content = content


# Define MeterReading model
class MeterReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=default_datetime, nullable=False)
    customer_name = db.Column(db.String(50))
    house_section = db.Column(db.String(50))
    house_number = db.Column(db.String(20))
    reading_value = db.Column(db.Float)
    consumed = db.Column(db.Float)
    unit_price = db.Column(db.Float)
    service_fee = db.Column(db.Float)
    sub_total_amount = db.Column(db.Float)
    total_amount = db.Column(db.Float)
    payment_status = db.Column(db.Boolean, default=False)
    unique_user_id = db.Column(db.String(6))

    # Specify foreign keys explicitly
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Establishing a one-to-many relationship with payments
    payments = db.relationship('Payment', backref='meter_reading', lazy=True)

    def __init__(self, reading_value, house_section, house_number, user_id, unit_price, service_fee, customer_name, consumed, sub_total_amount, total_amount, unique_user_id=None):
        self.house_section = house_section
        self.house_number = house_number
        self.reading_value = reading_value
        self.user_id = user_id
        self.customer_name = customer_name
        self.consumed = consumed
        self.unit_price = unit_price
        self.service_fee = service_fee
        self.sub_total_amount = sub_total_amount
        self.total_amount = total_amount
        self.unique_user_id = unique_user_id


# Define Payment model
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_amount = db.Column(db.Integer)
    customer_name = db.Column(db.String(50))
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=default_datetime, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    reference_number = db.Column(db.String(50))
    status = db.Column(db.Boolean, default=False)
    unique_user_id = db.Column(db.String(6))

    # Specify foreign keys explicitly
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey('meter_reading.id'), nullable=True)

    def __init__(self, customer_name, amount, timestamp, payment_method, user_id, reference_number=None, status=False, invoice_id=None, invoice_amount=None, unique_user_id=None):
        self.invoice_amount = invoice_amount
        self.customer_name = customer_name
        self.amount = amount
        self.timestamp = timestamp
        self.payment_method = payment_method
        self.reference_number = reference_number
        self.status = status
        self.user_id = user_id
        self.invoice_id = invoice_id
        self.unique_user_id = unique_user_id


# Define Expense model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=default_datetime, nullable=False)
    expense_type = db.Column(db.String(255), nullable=False)
    vendor = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float(), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def __init__(self, user_id, timestamp, expense_type, vendor, amount, description, status):
        self.user_id = user_id
        self.timestamp = timestamp
        self.expense_type = expense_type
        self.vendor = vendor
        self.amount = amount
        self.description = description
        self.status = status

    def __repr__(self):
        return f'<Expense {self.id}>'


# Define Message model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=default_datetime, nullable=False)
    is_read = db.Column(db.Boolean, default=False)

    def __init__(self, sender_id, receiver_id, content):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content


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


# Define Contact model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=default_datetime, nullable=False)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120))
    message = db.Column(db.Text)

    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message
