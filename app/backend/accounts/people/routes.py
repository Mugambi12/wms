from flask import Blueprint, render_template

peoples_bp = Blueprint('peoples', __name__, url_prefix='/peoples')

@peoples_bp.route('peoples/add_people')
def add_people():
    # You can add peoples-specific logic and data here
    return render_template('accounts/add_people.html', hide_footer=True)

@peoples_bp.route('peoples/people_list')
def people_list():
    # You can add peoples-specific logic and data here
    return render_template('accounts/people_list.html', hide_footer=True)
