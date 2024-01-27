from flask import Blueprint, render_template

security_bp = Blueprint('security', __name__, url_prefix='/security')

@security_bp.route('/security_options')
def security_options():
    # You can add security-specific logic and data here
    return render_template('accounts/security_options.html', hide_footer=True)
