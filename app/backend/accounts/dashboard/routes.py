# app/backend/accounts/dashboard/routes.py

from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ...database.models import User, MeterReading, Payment, Note
from app import db
from .forms import StickyNoteForm


dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


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


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    now = datetime.utcnow() + timedelta(hours=3)
    # Query data from the database
    people_list = User.query.all()
    total_houses = User.query.count()
    total_revenue = sum(payment.amount for payment in Payment.query.all())
    total_consumption = sum(reading.consumed for reading in MeterReading.query.all())
    total_expenses = sum(expense.amount for expense in Payment.query.filter_by(status=True))

    invoices = MeterReading.query.all()

    content_form = StickyNoteForm()
    sticky_note_content = Note.query.all()

    return render_template('accounts/dashboard.html',
                            now=now,
                            people_list=people_list,
                            total_houses=total_houses,
                            total_revenue=total_revenue,
                            total_consumption=total_consumption,
                            total_expenses=total_expenses,
                            hide_footer=True,
                            invoices=invoices,
                            content_form=content_form,
                            sticky_note_content=sticky_note_content)


@dashboard_bp.route('/save_sticky_note', methods=['POST'])
@login_required
def save_sticky_note():
    if request.method == 'POST':
        content = request.form.get('content')
        update_sticky_note_content(content)
        return '', 204
    flash('Failed to update sticky note.', 'danger')
    return redirect(url_for('accounts.dashboard.dashboard'))
