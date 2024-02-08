# app/backend/accounts/accounts_context.py
from flask import g
from datetime import datetime, timedelta, timezone
from ..models.user import Settings

def accounts_context():
    settings = Settings.query.first()
    get_company_name = settings.company_name
    company_name = get_company_name if get_company_name else 'ApoGen'

    bill = int('2500')

    return {
        'company_name': company_name,
        'bill': bill
        }


def inject_now():
    return {'now': datetime.utcnow() + timedelta(hours=3)}
