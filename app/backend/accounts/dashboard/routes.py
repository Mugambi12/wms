# app/backend/accounts/dashboard/routes.py

from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ...database.models import User, Note, MeterReading, Payment, Expense
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

def get_user_list(current_user):
    now = datetime.utcnow() + timedelta(hours=3)

    if current_user.is_admin:
        users_to_display = User.query.filter_by(is_admin=True).all()
    else:
        users_to_display = User.query.filter_by(house_section=current_user.house_section, house_number=current_user.house_number).all()

    return now, users_to_display


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    # Get dashboard cards data
    cards_data = dashboard_cards_data()

    # Get data for the list of users
    now, users_to_display = get_user_list(current_user)

    # Sticky Notes Logic and Data
    content_form = StickyNoteForm()
    sticky_note_content = Note.query.all()

    # Delinquent Bills Data
    invoices = MeterReading.query.all()

    return render_template('accounts/dashboard.html',
                           cards_data=cards_data,

                            now=now,
                            users_to_display=users_to_display,

                            content_form=content_form,
                            sticky_note_content=sticky_note_content,

                            invoices=invoices,

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
