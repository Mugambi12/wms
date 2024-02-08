# app/backend/accounts/accounts_context.py
from flask import g
from datetime import datetime, timedelta, timezone
from ..models.user import Settings

def accounts_context():
    # Retrieve the company name from the database
    company = Settings.query.first()
    company_name = company.company_name if company else 'ApoGen'

    bill = int('2500')

    return {'company_name': company_name, 'bill': bill}


def inject_now():
    return {'now': datetime.utcnow() + timedelta(hours=3)}
