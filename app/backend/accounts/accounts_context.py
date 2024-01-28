# app/backend/accounts/accounts_context.py
from flask import g
from datetime import datetime, timedelta, timezone

def accounts_context():
    people = 'silas'
    bill = int('2500')
    return {'people': people, 'bill': bill}

def inject_now():
    return {'now': datetime.utcnow() + timedelta(hours=3)}
