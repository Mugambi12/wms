from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/overview')
def dashboard():
    # You can add dashboard-specific logic and data here
    return render_template('dashboard/overview.html', hide_footer=True)

@dashboard_bp.route('peoples/add_people')
def add_people():
    # You can add dashboard-specific logic and data here
    return render_template('dashboard/add_people.html', hide_footer=True)

@dashboard_bp.route('peoples/people_list')
def people_list():
    # You can add dashboard-specific logic and data here
    return render_template('dashboard/people_list.html', hide_footer=True)

@dashboard_bp.route('records/meter_readings')
def meter_readings():
    # You can add dashboard-specific logic and data here
    return render_template('dashboard/meter_readings.html', hide_footer=True)

@dashboard_bp.route('records/billing')
def billing():
    # You can add dashboard-specific logic and data here
    return render_template('dashboard/billing.html', hide_footer=True)

@dashboard_bp.route('records/payments')
def payments():
    # You can add dashboard-specific logic and data here
    return render_template('dashboard/billing.html', hide_footer=True)

@dashboard_bp.route('/messages')
def messages():
    # You can add dashboard-specific logic and data here
    return render_template('dashboard/messages.html', hide_footer=True)

@dashboard_bp.route('/settings')
def settings():
    # You can add dashboard-specific logic and data here
    return render_template('dashboard/settings.html', hide_footer=True)

@dashboard_bp.route('/security_options')
def security_options():
    # You can add dashboard-specific logic and data here
    return render_template('dashboard/security_options.html', hide_footer=True)
