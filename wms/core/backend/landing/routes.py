from flask import Blueprint
from .utils import _landing, _submit_message


landing_bp = Blueprint('landing', __name__)


@landing_bp.route('/')
def landing():
    return _landing()


@landing_bp.route('/submit_message', methods=['POST'])
def submit_message():
    return _submit_message()
