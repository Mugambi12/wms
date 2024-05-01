# File: app/backend/accounts/dashboard/utils.py

# Import necessary libraries and modules
from datetime import datetime, timedelta
from flask_login import current_user
from sqlalchemy import func, extract
from ...database.models import *
from core import db


def dashboard_cards_data(current_user):
    if current_user.is_admin:
        total_houses = User.query.filter(
                            (User.house_section != 'admin') &
                            (User.house_section != 'Admin') &
                            (User.house_section.isnot(None)) &
                            User.house_number.isnot(None)
                        ).with_entities(User.house_section, User.house_number).distinct().count()
        total_revenue = sum(payment.amount for payment in Payment.query.all())
        total_consumption = sum(reading.consumed for reading in MeterReading.query.all())
        total_expenses = sum(expense.amount for expense in Expense.query.all())
    else:
        total_houses = User.query.filter(User.house_section == current_user.house_section, User.house_number == current_user.house_number).with_entities(User.house_section, User.house_number).distinct().count()
        total_revenue = sum(payment.amount for payment in Payment.query.filter_by(user_id=current_user.id).all())
        total_consumption = sum(reading.consumed for reading in MeterReading.query.filter(MeterReading.user_id == current_user.id).all())
        total_expenses = sum(reading.total_amount for reading in MeterReading.query.filter(MeterReading.user_id == current_user.id, MeterReading.payment_status == False).all())

    cards_data = {
        'total_houses': total_houses,
        'total_revenue': total_revenue,
        'total_consumption': total_consumption,
        'total_expenses': total_expenses
    }

    return cards_data


def fetch_monthly_performance_data(current_user, month, year):
    if current_user.is_admin:
        revenue_generated = db.session.query(func.sum(Payment.amount)) \
                                       .filter(extract('month', Payment.timestamp) == month) \
                                       .filter(extract('year', Payment.timestamp) == year) \
                                       .scalar() or 0

        water_consumed = db.session.query(func.sum(MeterReading.consumed)) \
                                    .filter(extract('month', MeterReading.timestamp) == month) \
                                    .filter(extract('year', MeterReading.timestamp) == year) \
                                    .scalar() or 0
    else:
        revenue_generated = db.session.query(func.sum(Payment.amount)) \
                                       .join(User) \
                                       .filter(User.id == current_user.id) \
                                       .filter(extract('month', Payment.timestamp) == month) \
                                       .filter(extract('year', Payment.timestamp) == year) \
                                       .scalar() or 0

        water_consumed = db.session.query(func.sum(MeterReading.consumed)) \
                                    .join(User) \
                                    .filter(User.id == current_user.id) \
                                    .filter(extract('month', MeterReading.timestamp) == month) \
                                    .filter(extract('year', MeterReading.timestamp) == year) \
                                    .scalar() or 0

    return revenue_generated, water_consumed


def fetch_bar_chart_data(current_user):
    if current_user.is_admin:
        usage_data = db.session.query(func.sum(MeterReading.consumed).label('consumed'), extract('month', MeterReading.timestamp).label('month')) \
                                 .group_by(extract('month', MeterReading.timestamp)) \
                                 .all()

        revenue_data = db.session.query(func.sum(Payment.amount).label('total_amount'), extract('month', Payment.timestamp).label('month')) \
                                 .group_by(extract('month', Payment.timestamp)) \
                                 .all()

        expense_data = db.session.query(func.sum(Expense.amount).label('total_amount'), extract('month', Expense.timestamp).label('month')) \
                                 .group_by(extract('month', Expense.timestamp)) \
                                 .all()
    else:
        usage_data = db.session.query(func.sum(MeterReading.consumed).label('consumed'), extract('month', MeterReading.timestamp).label('month')) \
                                 .join(User) \
                                 .filter(User.id == current_user.id) \
                                 .group_by(extract('month', MeterReading.timestamp)) \
                                 .all()

        revenue_data = db.session.query(func.sum(Payment.amount).label('total_amount'), extract('month', Payment.timestamp).label('month')) \
                                 .join(User) \
                                 .filter(User.id == current_user.id) \
                                 .group_by(extract('month', Payment.timestamp)) \
                                 .all()

        expense_data = []

    usage_dict = {result.month: result.consumed for result in usage_data}
    revenue_dict = {result.month: result.total_amount for result in revenue_data}
    expense_dict = {result.month: result.total_amount for result in expense_data}

    combined_data = {}
    for month in range(1, 13):
        combined_data[month] = {'usage': usage_dict.get(month, 0), 'revenue': revenue_dict.get(month, 0), 'expenses': expense_dict.get(month, 0)}

    return combined_data


def fetch_doughnut_chart_data(current_user):
    if current_user.is_admin:
        total_unpaid_invoices = sum(invoice.total_amount for invoice in MeterReading.query.filter_by(payment_status=False).all())
        total_unverified_payments = sum(payment.amount for payment in Payment.query.filter_by(status=False).all())
    else:
        total_unpaid_invoices = sum(invoice.total_amount for invoice in MeterReading.query.filter_by(payment_status=False, user_id=current_user.id).all())
        total_unverified_payments = sum(payment.amount for payment in Payment.query.filter_by(status=False, user_id=current_user.id).all())

    combined_data = {
        "Unpaid Invoices": total_unpaid_invoices,
        "Unverified Payments": total_unverified_payments
    }

    return combined_data


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
                                      .group_by(MeterReading.customer_name,
                                                MeterReading.house_section,
                                                MeterReading.house_number,
                                                MeterReading.consumed,
                                                MeterReading.service_fee,
                                                User.balance) \
                                      .all()
    else:
        user_id = current_user.id

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
                                              User.id == user_id) \
                                      .group_by(MeterReading.customer_name,
                                                MeterReading.house_section,
                                                MeterReading.house_number,
                                                MeterReading.consumed,
                                                MeterReading.service_fee,
                                                User.balance) \
                                      .all()

    return household_invoices


def recent_transactions_data(current_user):
    if current_user.is_admin:
        meter_readings = MeterReading.query.all()
        payments = Payment.query.all()
        expenses = Expense.query.all()
    else:
        meter_readings = MeterReading.query.filter_by(user_id=current_user.id).all()
        payments = Payment.query.filter_by(user_id=current_user.id).all()
        expenses = Expense.query.filter_by(user_id=current_user.id).all()

    meter_readings_with_type = [(meter_reading, 'MeterReading') for meter_reading in meter_readings]
    payments_with_type = [(payment, 'Payment') for payment in payments]
    expenses_with_type = [(expense, 'Expense') for expense in expenses]

    all_transactions = meter_readings_with_type + payments_with_type + expenses_with_type

    sorted_transactions = sorted(all_transactions, key=lambda x: x[0].timestamp, reverse=True)

    return sorted_transactions


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
