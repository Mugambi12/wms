# File: app/backend/accounts/dashboard/routes.py

# Import necessary libraries and modules
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ...database.models import *
from .forms import StickyNoteForm
from .utils import *


dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        current_month = int(request.form['current_month'])
        current_year = int(request.form['current_year'])
    else:
        today = datetime.now()
        current_month = today.month
        current_year = today.year

    cards_data = dashboard_cards_data(current_user)

    current_monthly_performance = fetch_monthly_performance_data(current_user, current_month, current_year)

    previous_month = current_month - 1 if current_month != 1 else 12
    previous_year = current_year - 1 if current_month == 1 else current_year

    next_month = current_month + 1 if current_month != 12 else 1
    next_year = current_year + 1 if current_month == 12 else current_year

    bar_chart_data = fetch_bar_chart_data(current_user)

    doughnut_chart_data = fetch_doughnut_chart_data(current_user)

    recent_transactions = recent_transactions_data(current_user)

    now, users_to_display = get_user_list(current_user)

    content_form = StickyNoteForm()
    sticky_note_content = Note.query.all()

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
                           bar_chart_data=bar_chart_data,
                           doughnut_chart_data=doughnut_chart_data,
                           recent_transactions=recent_transactions,
                           now=now,
                           users_to_display=users_to_display,
                           content_form=content_form,
                           sticky_note_content=sticky_note_content,
                           household_invoices=household_invoices,
                           hide_footer=True,
                           title="Dashboard")


@dashboard_bp.route('/save_sticky_note', methods=['POST'])
@login_required
def save_sticky_note():
    if request.method == 'POST':
        content = request.form.get('content')
        update_sticky_note_content(content)
        return '', 204
    flash('Failed to update sticky note.', 'danger')
    return redirect(url_for('accounts.dashboard.dashboard'))
