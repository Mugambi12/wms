import os
from datetime import timedelta
from secrets import token_hex

class Config:
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///watermanagement.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session settings
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1.5)

    # Debug mode
    DEBUG = True

    # Server settings
    PORT = 5000
    HOST = '0.0.0.0'

    # Mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    #MAIL_USERNAME = 'silasmungiria.sm@gmail.com'
    #MAIL_PASSWORD = 'dcjr nask mhqs xoyj'
    MAIL_USERNAME = 'apogen.ss@gmail.com'
    MAIL_PASSWORD = 'zowv rzzn kzsb dtgs'
    #MAIL_PASSWORD = 'cldn ewhn hfse ccyu'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # Generate a secure secret key
    SECRET_KEY = os.getenv('SECRET_KEY', token_hex(16))

    # Logging configuration
    LOG_FILE = 'app.log'
    LOG_LEVEL = 'DEBUG'

    # Error handling configuration
    ERROR_404_HELP = False

    # Security settings
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = os.getenv('CSRF_SESSION_KEY', token_hex(16))
    WTF_CSRF_TIME_LIMIT = None
    WTF_CSRF_ENABLED = True
    CORS_HEADERS = 'Content-Type'
