# app/backend/models/user.py
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin

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

    # Establishing a one-to-many relationship with records
    records = db.relationship('Record', backref='user', lazy=True)

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

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meter_reading = db.Column(db.Float)
    billing_info = db.Column(db.String(255))
    payment_info = db.Column(db.String(255))

    def __init__(self, meter_reading, billing_info, payment_info, user_id):
        self.user_id = user_id
        self.meter_reading = meter_reading
        self.billing_info = billing_info
        self.payment_info = payment_info
