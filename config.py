# app/config.py

from datetime import timedelta
from decouple import config

class MailConfig:
    MAIL_SERVER = config('MAIL_SERVER', default='smtp.gmail.com')
    MAIL_PORT = config('MAIL_PORT', default=465, cast=int)
    MAIL_USERNAME = config('MAIL_USERNAME')
    MAIL_PASSWORD = config('MAIL_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    MAIL_SUPPRESS_SEND = False
    MAIL_DEBUG = False
    MAIL_FAIL_SILENTLY = False


class Config:
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)
    PORT = config('PORT')
    HOST = config('HOST')

    CSRF_ENABLED = config('CSRF_ENABLED', cast=bool)
    CSRF_SESSION_KEY = config('CSRF_SESSION_KEY')
    WTF_CSRF_TIME_LIMIT = None
    WTF_CSRF_ENABLED = True


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = config('DEVELOPMENT_DATABASE_URI')
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SESSION_COOKIE_SECURE = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1.5)


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = config('PRODUCTION_DATABASE_URI')
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1.5)


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = config('TEST_DATABASE_URI')
    SQLALCHEMY_ECHO = False
    TESTING = True
