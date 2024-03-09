# File: config.py

import os
from datetime import timedelta
from secrets import token_hex

class Config:
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///watermanagement.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1.5)
    DEBUG = True
    PORT = 5000
    HOST = '0.0.0.0'

    # Mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'silasmungiria.sm@gmail.com'
    MAIL_PASSWORD = 'cldn ewhn hfse ccyu'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # Generate a secure secret key
    SECRET_KEY = os.getenv('SECRET_KEY', token_hex(16))
