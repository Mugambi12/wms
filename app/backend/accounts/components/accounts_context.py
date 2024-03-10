# File: app/backend/accounts/accounts_context.py


from datetime import datetime, timedelta
from ...database.models import User, CompanyInformation, PaymentMethods
from ..messages.utils import get_unread_message_count_for_navbar


def accounts_context():
    all_users = User.query.all()
    unread_message_counts = {user.id: get_unread_message_count_for_navbar(user.id) for user in all_users}

    servicesettings = CompanyInformation.query.first()
    company_name = servicesettings.company_name if servicesettings and servicesettings.company_name is not None else 'Apo Gen'
    contact_number = servicesettings.contact_number if servicesettings and servicesettings.contact_number is not None else '723396403'

    paymentmethods = PaymentMethods.query.first()
    bank_name = paymentmethods.bank_name if paymentmethods and paymentmethods.bank_name is not None else 'M-Pesa'
    paybill = paymentmethods.paybill if paymentmethods and paymentmethods.paybill is not None else 'N/A'
    account_number = paymentmethods.account_number if paymentmethods and paymentmethods.account_number is not None else '254723396403'

    return {
        'unread_message_counts': unread_message_counts,
        'company_name': company_name,
        'contact_number': contact_number,
        'bank_name': bank_name,
        'paybill': paybill,
        'account_number': account_number,
    }


def inject_now():
    return {'now': datetime.utcnow() + timedelta(hours=3)}
