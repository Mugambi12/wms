# File: app/backend/accounts/accounts_context.py


from datetime import datetime, timedelta, timezone
from sqlalchemy import func
from app import db
from ...database.models import User, MeterReading, Settings
from ..messages.utils import get_unread_message_count_for_navbar


def accounts_context():
    settings = Settings.query.first()


    all_users = User.query.all()
    unread_message_counts = {user.id: get_unread_message_count_for_navbar(user.id) for user in all_users}

    company_name = settings.company_name if settings else 'ApoGen'
    bank_name = settings.bank_name if settings else 'M-Pesa'
    paybill = settings.paybill if settings else '123456'
    account_number = settings.account_number if settings else '123456789'
    contact_number = settings.contact_number if settings else '0722000111'

    # Calculate total bill for each user with false status reading
    total_bill = db.session.query(func.sum(MeterReading.total_price)).filter(MeterReading.reading_status == False).scalar()
    total_bill = total_bill or 0

    return {
        'unread_message_counts': unread_message_counts,

        'company_name': company_name,
        'bank_name': bank_name,
        'paybill': paybill,
        'account_number': account_number,
        'contact_number': contact_number,
        'total_bill': total_bill
    }

def inject_now():
    return {'now': datetime.utcnow() + timedelta(hours=3)}
