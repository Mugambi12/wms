# File: app/backend/accounts/accounts_context.py


from datetime import datetime, timedelta
from ...database.models import User, CompanyInformation, PaymentMethods, SocialAccounts, CompanyInformation
from ..messages.utils import get_unread_message_count_for_navbar


def inject_now():
    return {'now': datetime.utcnow() + timedelta(hours=3)}


def accounts_context():
    # Retrieve all users and unread message counts
    all_users = User.query.all()
    unread_message_counts = {user.id: get_unread_message_count_for_navbar(user.id) for user in all_users}

    # Retrieve company information
    company_information = CompanyInformation.query.first()
    company_logo = getattr(company_information, 'company_logo', '')
    company_name = getattr(company_information, 'company_name', "Dakoke Springs")
    company_address = getattr(company_information, 'company_address', 'Nairobi')
    contact_number = getattr(company_information, 'contact_number', '254720352846')
    company_email = getattr(company_information, 'company_email', 'info@dakokesprings.co.ke')
    company_website_url = getattr(company_information, 'company_website_url', 'http://www.dakokesprings.co.ke')
    company_description = getattr(company_information, 'company_description', 'Welcome to dakoke springs. The best water service solutions company.')

    # Retrieve payment methods
    payment_methods = PaymentMethods.query.first()
    bank_name = getattr(payment_methods, 'bank_name', 'Cooperative Bank of Kenya')
    paybill = getattr(payment_methods, 'paybill', '400200')
    account_number = getattr(payment_methods, 'account_number', '40003937')
    account_name = getattr(payment_methods, 'account_name', 'Venter Nkatha')

    # Retrieve social links
    social_links = SocialAccounts.query.first()
    whatsapp = getattr(social_links, 'whatsapp', 'https://www.whatsapp.com/')
    facebook = getattr(social_links, 'facebook', 'https://www.facebook.com/')
    youtube = getattr(social_links, 'youtube', 'https://www.youtube.com/')
    twitter = getattr(social_links, 'twitter', 'https://twitter.com/')
    instagram = getattr(social_links, 'instagram', 'https://www.instagram.com/')
    linkedin = getattr(social_links, 'linkedin', 'https://www.linkedin.com/')
    tiktok = getattr(social_links, 'tiktok', 'https://www.tiktok.com/')

    # Return a dictionary with all relevant data
    return {
        'all_users': all_users,
        'unread_message_counts': unread_message_counts,

        'company_logo': company_logo,
        'company_name': company_name,
        'company_address': company_address,
        'contact_number': contact_number,
        'company_email': company_email,
        'company_website_url': company_website_url,
        'company_description': company_description,

        'bank_name': bank_name,
        'paybill': paybill,
        'account_number': account_number,
        'account_name': account_name,

        'whatsapp': whatsapp,
        'facebook': facebook,
        'youtube': youtube,
        'twitter': twitter,
        'instagram': instagram,
        'linkedin': linkedin,
        'tiktok': tiktok
    }

