# File: app/backend/accounts/accounts_context.py


from datetime import datetime, timedelta
from ...database.models import User, CompanyInformation, PaymentMethods, SocialAccounts, CompanyInformation
from ..messages.utils import get_unread_message_count_for_navbar


def inject_now():
    return {'now': datetime.utcnow() + timedelta(hours=3)}


def accounts_context():
    all_users = User.query.all()
    unread_message_counts = {user.id: get_unread_message_count_for_navbar(user.id) for user in all_users}


    company_information = CompanyInformation.query.first()
    company_logo = ''
    if company_information and company_information.company_logo is not None:
        company_logo = company_information.company_logo

    company_name = company_information.company_name if company_information and company_information.company_name is not None else 'ApoGen io'
    company_address = company_information.company_address if company_information and company_information.company_address is not None else 'Nairobi'
    contact_number = company_information.contact_number if company_information and company_information.contact_number is not None else '254723396403'
    company_email = company_information.company_email if company_information and company_information.company_email is not None else 'info@apogen.io'
    company_website_url = company_information.company_website_url if company_information and company_information.company_website_url is not None else 'http://www.apogen.io'
    company_description = company_information.company_description if company_information and company_information.company_description is not None else 'Welcome to apogen. The best software solutions company in Africa.'

    payment_methods = PaymentMethods.query.first()
    bank_name = payment_methods.bank_name if payment_methods and payment_methods.bank_name is not None else 'ApoGen QuickPay'
    paybill = payment_methods.paybill if payment_methods and payment_methods.paybill is not None else 'N/A'
    account_number = payment_methods.account_number if payment_methods and payment_methods.account_number is not None else '254723396403'

    social_links = SocialAccounts.query.first()
    whatsapp = social_links.whatsapp if social_links and social_links.whatsapp is not None else 'https://www.whatsapp.com/'
    facebook = social_links.facebook if social_links and social_links.facebook is not None else 'https://www.facebook.com/'
    youtube = social_links.youtube if social_links and social_links.youtube is not None else 'https://www.youtube.com/'
    twitter = social_links.twitter if social_links and social_links.twitter is not None else 'https://twitter.com/'
    instagram = social_links.instagram if social_links and social_links.instagram is not None else 'https://www.instagram.com/'
    linkedin = social_links.linkedin if social_links and social_links.linkedin is not None else 'https://www.linkedin.com/'
    tiktok = social_links.tiktok if social_links and social_links.tiktok is not None else 'https://www.tiktok.com/'


    return {
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

        'whatsapp': whatsapp,
        'facebook': facebook,
        'youtube': youtube,
        'twitter': twitter,
        'instagram': instagram,
        'linkedin': linkedin,
        'tiktok': tiktok
    }
