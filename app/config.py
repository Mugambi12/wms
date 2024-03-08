import os
from datetime import timedelta
#from dotenv import load_dotenv
from secrets import token_hex

# File: config.py


# Load environment variables from .env file
#load_dotenv()

class Config:
    # Other configuration options...

    # Database settings
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///watermanagement.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1.5)
    DEBUG = True

    # Mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    #MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    #MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USERNAME = 'silasmungiria.sm@gmail.com'
    MAIL_PASSWORD = 'plrj pmhi wffz xwxu'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # Generate a secure secret key
    SECRET_KEY = os.getenv('SECRET_KEY', token_hex(16))
