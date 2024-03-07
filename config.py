# File: config.py

# Import necessary modules
from datetime import timedelta
from app.utils import generate_random_string

class Config:
    # Other configuration options...

    # Database settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///watermanagement.db'
    # Replace 'your_username', 'your_password', 'localhost', and 'your_database' with your MySQL credentials
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://apogen:Apogen2023@localhost/watermanagement'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1.5)
    # SESSION_COOKIE_SECURE = True
    SECRET_KEY = generate_random_string()

    # Mail settings
    MAIL_SERVER = 'smtp.example.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'silasmungiria16@gmail.com'
    MAIL_PASSWORD = '153O9101o24'
    MAIL_DEFAULT_SENDER = 'silasmungiria16@gmail.com'
