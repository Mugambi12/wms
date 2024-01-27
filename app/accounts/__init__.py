from flask import Blueprint

def accounts_context():
    people = 'silas'
    bill = int('2500')
    return {'people': people, 'bill': bill}

accounts_bp = Blueprint('accounts', __name__)

# You can add any necessary initialization code for the accounts module here
