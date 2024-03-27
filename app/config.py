import os
from datetime import timedelta
from secrets import token_hex

class Config:
    # MySQL Database settings
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://foo:foo123@localhost/watermanagement'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SQLAlchemy Database settings
    #SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///watermanagementsystem.db')
    #SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session settings
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1.5)

    # Debug mode
    DEBUG = True

    # Server settings
    PORT = 2023
    HOST = '0.0.0.0'

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

# Mail settings
server = 'smtp.gmail.com'
email = 'apogen.ss@gmail.com'
passcode = 'zowv rzzn kzsb dtgs'

class MailConfig:
    # Mail settings
    MAIL_SERVER = server
    MAIL_PORT = 465
    MAIL_USERNAME = email
    MAIL_PASSWORD = passcode
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    MAIL_SUPPRESS_SEND = False
    MAIL_DEBUG = False
    MAIL_FAIL_SILENTLY = False
