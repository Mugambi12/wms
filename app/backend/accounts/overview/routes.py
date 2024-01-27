from flask import Blueprint, render_template

overview_bp = Blueprint('overview', __name__, url_prefix='/overview')

@overview_bp.route('/overview')
def overview():
    # You can add overview-specific logic and data here
    return render_template('accounts/overview.html', hide_footer=True)
