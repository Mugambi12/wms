from flask import Blueprint, render_template

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

@settings_bp.route('/settings')
def settings():
    # You can add settings-specific logic and data here
    return render_template('accounts/settings.html', hide_footer=True)
