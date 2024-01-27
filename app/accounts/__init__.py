from flask import Blueprint

def dashboard_context():
    people = 'silas'
    bill = int('2500')
    return {'people': people, 'bill': bill}

dashboard_bp = Blueprint('dashboard', __name__)

# You can add any necessary initialization code for the dashboard module here
