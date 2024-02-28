# File: app/backend/accounts/accounts_context.py


from datetime import datetime, timedelta
from ...database.models import User, Settings
from ..messages.utils import get_unread_message_count_for_navbar


def accounts_context():
    all_users = User.query.all()
    unread_message_counts = {user.id: get_unread_message_count_for_navbar(user.id) for user in all_users}

    settings = Settings.query.first()
    company_name = settings.company_name if settings and settings.company_name is not None else 'ApoGen'
    bank_name = settings.bank_name if settings and settings.bank_name is not None else 'M-Pesa'
    paybill = settings.paybill if settings and settings.paybill is not None else 'N/A'
    account_number = settings.account_number if settings and settings.account_number is not None else '254723396403'
    contact_number = settings.contact_number if settings and settings.contact_number is not None else '723396403'

    return {
        'unread_message_counts': unread_message_counts,
        'company_name': company_name,
        'bank_name': bank_name,
        'paybill': paybill,
        'account_number': account_number,
        'contact_number': contact_number,
    }


def inject_now():
    return {'now': datetime.utcnow() + timedelta(hours=3)}
