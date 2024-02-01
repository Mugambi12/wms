# app/backend/models/user.py
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from datetime import datetime, timedelta, timezone

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

    # Establishing a one-to-many relationship with meter readings and payments
    meter_readings = db.relationship('MeterReading', backref='user', lazy=True)
    payments = db.relationship('Payment', backref='user', lazy=True)

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


class MeterReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc) + timedelta(hours=3), nullable=False)
    house_section = db.Column(db.String(50))
    house_number = db.Column(db.String(20))
    reading_value = db.Column(db.Float)
    reading_status = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, reading_value, house_section, house_number, user_id):
        self.house_section = house_section
        self.house_number = house_number
        self.reading_value = reading_value
        self.user_id = user_id


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    payment_method = db.Column(db.String(50))
    reference_number = db.Column(db.String(50))
    status = db.Column(db.String(20))  # e.g., "Pending", "Processed"
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, amount, payment_date, user_id, payment_method=None, reference_number=None, status="Pending"):
        self.amount = amount
        self.payment_date = payment_date
        self.user_id = user_id
        self.payment_method = payment_method
        self.reference_number = reference_number
        self.status = status

    def mark_as_processed(self):
        self.status = "Processed"

    def __repr__(self):
        return f"<Payment {self.id}: {self.amount} {self.payment_date}>"


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit_price = db.Column(db.Float)
    house_sections = db.Column(db.String(255))

    def __init__(self, unit_price=None, house_sections=None):
        self.unit_price = unit_price
        self.house_sections = house_sections


