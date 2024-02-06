# app/backend/accounts/records/routes.py
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from app import db
from .forms import AddMeterReadingForm, EditMeterReadingForm
from ...models.user import MeterReading, User, Settings
from .meter_readings import handle_add_meter_reading, get_meter_readings, edit_meter_reading_logic, delete_meter_reading_logic

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
    if current_user.is_authenticated:
        edited_reading = MeterReading.query.get_or_404(meter_reading_id)

        result = edit_meter_reading_logic(edited_reading)

        if result['success']:
            flash(result['message'], 'success')
            return redirect(url_for('accounts.records.meter_readings'))
        else:
            flash(result['message'], 'danger')
            return render_template('accounts/meter_readings.html', form=result['form'], meter_reading=edited_reading, hide_footer=True)
    else:
        return redirect(url_for('auth.login'))


@records_bp.route('/delete_meter_reading/<int:meter_reading_id>', methods=['POST'])
@login_required
def delete_meter_reading(meter_reading_id):
    if current_user.is_authenticated:
        result = delete_meter_reading_logic(meter_reading_id)

        if result['success']:
            flash(result['message'], 'success')
        else:
            flash(result['message'], 'danger')

        return redirect(url_for('accounts.records.meter_readings'))
    else:
        return redirect(url_for('auth.login'))
















from sqlalchemy import func

def fetch_billing_data():
    get_billing_data = (
            db.session.query(
                MeterReading.id,
                MeterReading.timestamp,
                MeterReading.house_section,
                MeterReading.house_number,
                MeterReading.reading_status,
                MeterReading.customer_name,
                func.lag(MeterReading.reading_value)
                .over(partition_by=(MeterReading.house_section, MeterReading.house_number), order_by=MeterReading.timestamp)
                .label('prev_reading'),
                MeterReading.reading_value.label('curr_reading'),
                MeterReading.consumed,
                MeterReading.unit_price,
                MeterReading.sub_total_price,
                MeterReading.service_fee,
                MeterReading.total_price
            )
            .join(User)
            .filter(User.id == current_user.id)
            .order_by(MeterReading.timestamp.desc())
            .all()
        )
    return get_billing_data

@records_bp.route('/billing')
@login_required
def billing():
    if current_user.is_authenticated:
        billing_data = fetch_billing_data()

        return render_template('accounts/billing.html', hide_footer=True, billing_data=billing_data)
    else:
        return redirect(url_for('auth.login'))


def fetch_invoice_data(invoice_id):
    invoice = MeterReading.query.filter_by(id=invoice_id).first()
    if invoice:
        user = User.query.filter_by(id=invoice.user_id).first()

        service_qty = (
            MeterReading.query
            .filter(
                MeterReading.house_section == invoice.house_section,
                MeterReading.house_number == invoice.house_number,
                MeterReading.reading_status == False
            )
            .group_by(MeterReading.house_section, MeterReading.house_number)
            .count()
        )

        if user:
            invoice_data = {
                'mobile': user.mobile_number,
                'first_service': 'Water Usage',
                'first_description': 'Monthly water consumption',
                'second_service': 'Service Fee',
                'second_description': 'Maintenance & service charge',
                'invoice_id': invoice.id,
                'timestamp': invoice.timestamp,
                'customer_name': invoice.customer_name,
                'house_section': invoice.house_section,
                'house_number': invoice.house_number,
                'reading_value': invoice.reading_value,
                'unit_price': invoice.unit_price,
                'service_fee': invoice.service_fee,
                'consumed': invoice.consumed,
                'service_qty': service_qty,
                'sub_total_price': invoice.sub_total_price,
                'total_price': invoice.total_price,
                'reading_status': invoice.reading_status,
                'vat': '0'
            }
            return invoice_data
        else:
            return None
    else:
        return None



@records_bp.route('/invoice/<int:invoice_id>')
@login_required
def invoice(invoice_id):
    if current_user.is_authenticated:
        invoice_data = fetch_invoice_data(invoice_id)
        if invoice_data:
            # Pass invoice_data to the invoice template
            return render_template('accounts/invoice.html', invoice_data=invoice_data, hide_sidebar=True, hide_navbar=True, hide_footer=True)
        else:
            flash("Invoice not found", "error")
            return redirect(url_for('accounts.records.billing'))
    else:
        return redirect(url_for('auth.login'))






@records_bp.route('/payments')
@login_required
def payments():
    # Check if the user is still authenticated
    if current_user.is_authenticated:
        # You can add records-specific logic and data here
        return render_template('accounts/payments.html', hide_footer=True)
    else:
        # If the user is not authenticated, redirect to the login page
        return redirect(url_for('auth.login'))
