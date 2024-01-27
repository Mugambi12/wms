from flask import Blueprint, render_template


def admin_context():
    user = 'silas'
    bill = '2500'
    return {'user': user, 'bill': bill}


admin_bp = Blueprint('admin', __name__, url_prefix='/dashboard')

@admin_bp.route('/overview')
def dashboard():
    # You can add admin-specific logic and data here
    return render_template('admin/dashboard.html', hide_footer=True)

@admin_bp.route('users/add_user')
def add_user():
    # You can add admin-specific logic and data here
    return render_template('admin/add_user.html', hide_footer=True)

@admin_bp.route('users/user_list')
def user_list():
    # You can add admin-specific logic and data here
    return render_template('admin/user_list.html', hide_footer=True)

@admin_bp.route('records/consumption')
def consumption():
    # You can add admin-specific logic and data here
    return render_template('admin/consumption.html', hide_footer=True)

@admin_bp.route('records/billing')
def billing():
    # You can add admin-specific logic and data here
    return render_template('admin/billing.html', hide_footer=True)

@admin_bp.route('/messages')
def messages():
    # You can add admin-specific logic and data here
    return render_template('admin/messages.html', hide_footer=True)

@admin_bp.route('/settings')
def settings():
    # You can add admin-specific logic and data here
    return render_template('admin/settings.html', hide_footer=True)
