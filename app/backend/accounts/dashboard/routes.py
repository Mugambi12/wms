# File: app/backend/accounts/dashboard/routes.py

# Import necessary libraries and modules
from datetime import datetime, timedelta, timezone
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from sqlalchemy import func, extract
from ...database.models import *
from app import db
from .forms import StickyNoteForm


dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


def dashboard_cards_data():
    # Dashboard Cards Logic and Data
    total_houses = User.query.with_entities(User.house_section, User.house_number).distinct().count()
    total_revenue = sum(payment.amount for payment in Payment.query.all())
    total_consumption = sum(reading.consumed for reading in MeterReading.query.all())
    total_expenses = sum(expense.amount for expense in Expense.query.all())

    # Assemble the data into a dictionary
    cards_data = {
        'total_houses': total_houses,
        'total_revenue': total_revenue,
        'total_consumption': total_consumption,
        'total_expenses': total_expenses
    }

    return cards_data

def fetch_monthly_performance_data(month, year):
    revenue_generated = db.session.query(func.sum(Payment.amount)) \
                                   .filter(extract('month', Payment.timestamp) == month) \
                                   .filter(extract('year', Payment.timestamp) == year) \
                                   .scalar() or 0

    water_consumed = db.session.query(func.sum(MeterReading.consumed)) \
                                .filter(extract('month', MeterReading.timestamp) == month) \
                                .filter(extract('year', MeterReading.timestamp) == year) \
                                .scalar() or 0

    return revenue_generated, water_consumed

def fetch_bar_chart_data():
    # Fetch usage data from meter reading table and sum them by month
    usage_data = db.session.query(func.sum(MeterReading.consumed).label('consumed'), extract('month', MeterReading.timestamp).label('month')) \
                             .group_by(extract('month', MeterReading.timestamp)) \
                             .all()

    # Fetch revenue data from payments table and sum them by month
    revenue_data = db.session.query(func.sum(Payment.amount).label('total_amount'), extract('month', Payment.timestamp).label('month')) \
                             .group_by(extract('month', Payment.timestamp)) \
                             .all()

    # Fetch expense data from expenses table and sum them by month
    expense_data = db.session.query(func.sum(Expense.amount).label('total_amount'), extract('month', Expense.timestamp).label('month')) \
                             .group_by(extract('month', Expense.timestamp)) \
                             .all()

    # Format the data into dictionaries with month as key
    usage_dict = {result.month: result.consumed for result in usage_data}
    revenue_dict = {result.month: result.total_amount for result in revenue_data}
    expense_dict = {result.month: result.total_amount for result in expense_data}

    # Combine revenue and expenses data into a single dictionary
    combined_data = {}
    for month in range(1, 13):
        combined_data[month] = {'usage': usage_dict.get(month, 0), 'revenue': revenue_dict.get(month, 0), 'expenses': expense_dict.get(month, 0)}

    return combined_data

def fetch_doughnut_chart_data():
    total_unpaid_invoices = sum(invoice.total_amount for invoice in MeterReading.query.filter_by(payment_status=False).all())
    total_unverified_payments = sum(payment.amount for payment in Payment.query.filter_by(status=False).all())

    combined_data = {
        "Unpaid Invoices": total_unpaid_invoices,
        "Unverified Payments": total_unverified_payments
    }

    return combined_data

def recent_transactions_data():
    meter_readings = MeterReading.query.all()
    payments = Payment.query.all()
    expenses = Expense.query.all()

    # Add a type indicator to each transaction
    meter_readings_with_type = [(meter_reading, 'MeterReading') for meter_reading in meter_readings]
    payments_with_type = [(payment, 'Payment') for payment in payments]
    expenses_with_type = [(expense, 'Expense') for expense in expenses]

    # Combine all transactions with their types
    all_transactions = meter_readings_with_type + payments_with_type + expenses_with_type

    # Sort transactions by timestamp in descending order
    sorted_transactions = sorted(all_transactions, key=lambda x: x[0].timestamp, reverse=True)

    return sorted_transactions

def get_user_list(current_user):
    now = datetime.utcnow() + timedelta(hours=3)

    if current_user.is_admin:
        users_to_display = User.query.filter_by(is_admin=True).all()
    else:
        users_to_display = User.query.filter_by(house_section=current_user.house_section, house_number=current_user.house_number).all()

    return now, users_to_display

def delinquent_household_invoices(current_user):
    if current_user.is_admin:
        household_invoices = db.session.query(MeterReading.customer_name,
                                              MeterReading.house_section,
                                              MeterReading.house_number,
                                              MeterReading.consumed,
                                              func.sum(MeterReading.sub_total_amount).label('sub_total_amount'),
                                              MeterReading.service_fee,
                                              func.sum(MeterReading.total_amount).label('total_amount'),
                                              User.balance) \
                                      .join(User) \
                                      .filter(MeterReading.payment_status == False) \
                                      .group_by(MeterReading.house_section, MeterReading.house_number, User.balance) \
                                      .all()
    else:
        # Assuming user_role is stored in the user object
        user_house_section = current_user.house_section
        user_house_number = current_user.house_number

        household_invoices = db.session.query(MeterReading.customer_name,
                                              MeterReading.house_section,
                                              MeterReading.house_number,
                                              MeterReading.consumed,
                                              func.sum(MeterReading.sub_total_amount).label('sub_total_amount'),
                                              MeterReading.service_fee,
                                              func.sum(MeterReading.total_amount).label('total_amount'),
                                              User.balance) \
                                      .join(User) \
                                      .filter(MeterReading.payment_status == False,
                                              MeterReading.house_section == user_house_section,
                                              MeterReading.house_number == user_house_number) \
                                      .group_by(MeterReading.house_section, MeterReading.house_number, User.balance) \
                                      .all()

    return household_invoices

@dashboard_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        current_month = int(request.form['current_month'])
        current_year = int(request.form['current_year'])
    else:
        # Get current month and year
        today = datetime.now()
        current_month = today.month
        current_year = today.year

    # Get dashboard cards data
    cards_data = dashboard_cards_data()

    # Fetch monthly performance data for the current month
    current_monthly_performance = fetch_monthly_performance_data(current_month, current_year)

    # Define the previous month
    previous_month = current_month - 1 if current_month != 1 else 12
    previous_year = current_year - 1 if current_month == 1 else current_year

    # Define the next month
    next_month = current_month + 1 if current_month != 12 else 1
    next_year = current_year + 1 if current_month == 12 else current_year

    # Fetch actual revenue and expenses data from the database
    revenue_expense_data = fetch_bar_chart_data()

    # Fetch actual revenue and expenses data from the database
    doughnut_chart_data = fetch_doughnut_chart_data()

    # Get recent transactions data
    recent_transactions = recent_transactions_data()

    # Get data for the list of users
    now, users_to_display = get_user_list(current_user)

    # Prepare sticky notes data
    content_form = StickyNoteForm()
    sticky_note_content = Note.query.all()

    # Get delinquent bills data
    household_invoices = delinquent_household_invoices(current_user)

    return render_template('accounts/dashboard.html',
                           cards_data=cards_data,
                           current_monthly_performance=current_monthly_performance,
                           current_month=current_month,
                           current_year=current_year,
                           previous_month=previous_month,
                           previous_year=previous_year,
                           next_month=next_month,
                           next_year=next_year,
                           revenue_expense_data=revenue_expense_data,
                           doughnut_chart_data=doughnut_chart_data,
                           recent_transactions=recent_transactions,
                           now=now,
                           users_to_display=users_to_display,
                           content_form=content_form,
                           sticky_note_content=sticky_note_content,
                           household_invoices=household_invoices,
                           hide_footer=True)





@dashboard_bp.route('/save_sticky_note', methods=['POST'])
@login_required
def save_sticky_note():
    if request.method == 'POST':
        content = request.form.get('content')
        update_sticky_note_content(content)
        return '', 204
    flash('Failed to update sticky note.', 'danger')
    return redirect(url_for('accounts.dashboard.dashboard'))

def get_sticky_note_content():
    return Note.query.filter_by(user_id=current_user.id).first()

def update_sticky_note_content(new_content):
    new_content = ' '.join(new_content.split())

    sticky_note = get_sticky_note_content()
    if sticky_note:
        sticky_note.content = new_content
    else:
        sticky_note = Note(user_id=current_user.id, content=new_content)
        db.session.add(sticky_note)
    db.session.commit()
