# app/backend/accounts/accounts_context.py
from flask import g

def accounts_context():
    people = 'silas'
    bill = int('2500')
    return {'people': people, 'bill': bill}
