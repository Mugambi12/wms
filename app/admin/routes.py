from flask import Blueprint, render_template

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
def dashboard():
    user='silas'
    # You can add admin-specific logic and data here
    return render_template('admin/dashboard.html', user=user, hide_footer=True)

@admin_bp.route('/add_user')
def add_user():
    user='silas'
    # You can add admin-specific logic and data here
    return render_template('admin/add_user.html', user=user, hide_footer=True)

@admin_bp.route('/user_list')
def user_list():
    user='silas'
    # You can add admin-specific logic and data here
    return render_template('admin/user_list.html', user=user, hide_footer=True)

@admin_bp.route('/consumption')
def consumption():
    user='silas'
    # You can add admin-specific logic and data here
    return render_template('admin/consumption.html', user=user, hide_footer=True)

@admin_bp.route('/billing')
def billing():
    user='silas'
    # You can add admin-specific logic and data here
    return render_template('admin/billing.html', user=user, hide_footer=True)

@admin_bp.route('/messages')
def messages():
    user='silas'
    # You can add admin-specific logic and data here
    return render_template('admin/messages.html', user=user, hide_footer=True)

@admin_bp.route('/settings')
def settings():
    user='silas'
    # You can add admin-specific logic and data here
    return render_template('admin/settings.html', user=user, hide_footer=True)
