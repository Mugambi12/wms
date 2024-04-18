# File: app/utils.py

import secrets
import string

def generate_random_string(length=32):
    """
    Generate a random string of specified length using ASCII characters, digits, and punctuation.
    """
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def format_amount(value):
    """
    Format the given numeric value as a string representing an amount with commas for thousands separator.
    """
    return "{:,.0f}".format(value)
