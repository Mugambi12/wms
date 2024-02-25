# File: app/backend/accounts/expenses/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.backend.accounts.expenses.forms import AddExpenseForm
from app.backend.database.models import Expense, db
from datetime import datetime, timezone, timedelta

expenses_bp = Blueprint('expenses', __name__, url_prefix='/expenses')

@expenses_bp.route('/')
@login_required
def expenses():
    expenses = Expense.query.all()
    add_expense_form = AddExpenseForm()
    return render_template('accounts/expenses.html', expenses=expenses, add_expense_form=add_expense_form, hide_footer=True)

@expenses_bp.route('/add_expense', methods=['POST'])
@login_required
def add_expense():
    form = AddExpenseForm()
    if form.validate_on_submit():
        expense = Expense(
            user_id=current_user.id,
            timestamp=datetime.now(timezone.utc) + timedelta(hours=3),
            expense_type=form.expense_type.data,
            vendor=form.vendor.data,
            amount=form.amount.data,
            description=form.description.data,
            status=form.status.data
        )
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('accounts.expenses.expenses'))
    return render_template('accounts/expenses.html', add_expense_form=form, hide_footer=True)



@expenses_bp.route('/delete_expense/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    result = delete_expense_logic(expense_id)

    if result['success']:
        flash(result['message'], 'success')
    else:
        flash(result['message'], 'danger')

    return redirect(url_for('accounts.expenses.expenses'))


def delete_expense_logic(expense_id):
    try:
        expense = Expense.query.get(expense_id)

        if expense:
            db.session.delete(expense)
            db.session.commit()
            return {'success': True, 'message': 'Expense deleted successfully.'}
        else:
            return {'success': False, 'message': 'Expense not found.'}

    except Exception as e:
        return {'success': False, 'message': f'Error deleting expense: {str(e)}'}
