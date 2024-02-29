# File: app/backend/accounts/records/routes.py

# Import necessary libraries
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from app import db
from .forms import AddMeterReadingForm, EditMeterReadingForm, MakePaymentForm
from ...database.models import User, MeterReading
from .utils_meter_readings import handle_add_meter_reading, get_meter_readings, edit_meter_reading_logic, delete_meter_reading_logic
from .utils_billing import fetch_billing_data, fetch_invoice_data, fetch_payment_data
from .utils_payment_logic import make_payment_logic, delete_payment_logic


records_bp = Blueprint('records', __name__, url_prefix='/records')


@records_bp.route('/meter_readings', methods=['GET', 'POST'])
@login_required
def meter_readings():
    add_meter_reading_form = AddMeterReadingForm()
    edit_meter_reading_form = EditMeterReadingForm()

    if request.method == 'POST':
        form_type = request.form.get('form_type')

        if form_type == 'add':
            result = handle_add_meter_reading(add_meter_reading_form, current_user)

            if result['success']:
                flash(result['message'], 'success')
            else:
                flash(result['message'], 'danger')

    house_sections = db.session.query(User.house_section.distinct()).all()
    meter_readings = get_meter_readings(current_user)

    return render_template('accounts/meter_readings.html', house_sections=house_sections, meter_readings=meter_readings, form=add_meter_reading_form, edit_form=edit_meter_reading_form, hide_footer=True)


@records_bp.route('/edit_meter_reading/<int:meter_reading_id>', methods=['GET', 'POST'])
@login_required
def edit_meter_reading(meter_reading_id):
    edited_reading = MeterReading.query.get_or_404(meter_reading_id)

    result = edit_meter_reading_logic(edited_reading)

    if result['success']:
        flash(result['message'], 'success')
        return redirect(url_for('accounts.records.meter_readings'))
    else:
        flash(result['message'], 'danger')
        return render_template('accounts/meter_readings.html', form=result['form'], meter_reading=edited_reading, hide_footer=True)


@records_bp.route('/delete_meter_reading/<int:meter_reading_id>', methods=['POST'])
@login_required
def delete_meter_reading(meter_reading_id):
    result = delete_meter_reading_logic(meter_reading_id)

    if result['success']:
        flash(result['message'], 'success')
    else:
        flash(result['message'], 'danger')

    return redirect(url_for('accounts.records.meter_readings'))


@records_bp.route('/billing')
@login_required
def billing():
    billing_data = fetch_billing_data(current_user)
    make_payment_form = MakePaymentForm()

    return render_template('accounts/billing.html', make_payment=make_payment_form, billing_data=billing_data, payment_form=make_payment_form, hide_footer=True)


@records_bp.route('/make_payment/<int:payment_id>', methods=['GET', 'POST'])
@login_required
def make_payment(payment_id):
    meter_reading = MeterReading.query.get_or_404(payment_id)

    form = MakePaymentForm()

    if form.validate_on_submit():
        payment_amount = form.payment_amount.data
        payment_method = form.payment_method.data
        reference_number = form.reference_number.data
        status = form.status.data
        user_id = meter_reading.user_id

        result = make_payment_logic(
            meter_reading,
            payment_amount,
            payment_method,
            reference_number,
            status,
            user_id=user_id,
            invoice_amount=meter_reading.total_amount,
            invoice_id=meter_reading.id,
            unique_user_id=meter_reading.unique_user_id
        )

        if result['success']:
            flash(result['message'], 'success')
            return redirect(url_for('accounts.records.billing'))
        else:
            flash(result['message'], 'danger')

    return render_template('accounts/billing.html', form=form, meter_reading=meter_reading)


@records_bp.route('/invoice/<int:invoice_id>')
@login_required
def invoice(invoice_id):
    invoice_data = fetch_invoice_data(current_user, invoice_id)
    if invoice_data:
        return render_template('accounts/invoice.html', invoice_data=invoice_data, hide_sidebar=True, hide_navbar=True, hide_footer=True)
    else:
        flash("Invoice not found", "error")
        return redirect(url_for('accounts.records.billing'))


@records_bp.route('/payments')
@login_required
def payments():
    payment_data = fetch_payment_data(current_user)

    return render_template('accounts/payments.html', payment_data=payment_data, hide_footer=True)


@records_bp.route('/validate_payment/<int:payment_id>', methods=['POST'])
@login_required
def validate_payment(payment_id):
    result = validate_payment_logic(payment_id)

    if result['success']:
        flash(result['message'], 'success')
    else:
        flash(result['message'], 'danger')

    return redirect(url_for('accounts.records.payments'))

from ...database.models import Payment
def validate_payment_logic(payment_id):
    try:
        payment = Payment.query.get(payment_id)

        if payment:
            # Toggle payment status
            payment.status = not payment.status
            db.session.commit()

            return {'success': True, 'message': 'Payment status updated successfully.'}
        else:
            return {'success': False, 'message': 'Payment not found.'}

    except Exception as e:
        return {'success': False, 'message': f'Error updating payment status: {str(e)}'}




@records_bp.route('/delete_payment/<int:payment_id>', methods=['GET', 'POST'])
@login_required
def delete_payment(payment_id):
    result = delete_payment_logic(payment_id)

    if result['success']:
        flash(result['message'], 'success')
    else:
        flash(result['message'], 'danger')

    return redirect(url_for('accounts.records.payments'))


from ..components.download_manager import download_meter_readings

@records_bp.route('/download_meter_readings', methods=['GET'])
@login_required
def download_meter_readings_route():
    return download_meter_readings()


from ..components.download_manager import download_invoice

@records_bp.route('/download_invoice/<int:invoice_id>', methods=['GET'])
@login_required
def download_invoice_route(invoice_id):
    """
    Route to download an invoice PDF by its ID.

    Args:
        invoice_id (int): The ID of the invoice to be downloaded.

    Returns:
        Response: Flask response containing the invoice PDF file.

    """
    return download_invoice(invoice_id)
