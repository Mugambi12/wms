# File: app/backend/accounts/records/routes.py

from flask import Blueprint, flash, render_template, redirect, url_for, request, render_template_string, send_file, Response
from flask_login import login_required, current_user
from io import BytesIO
from xhtml2pdf import pisa

from core import db
from .forms import *
from ...database.models import *
from .utils_meter_readings import *
from .utils_payment_logic import make_payment_logic, delete_payment_logic, validate_payment_logic
from .utils_data import *
from ..components.payment_processor import process_payments_with_context
from ..components.download_manager import download_meter_readings, download_invoice


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

    return render_template('accounts/meter_readings.html',
                           house_sections=house_sections,
                           meter_readings=meter_readings,
                           form=add_meter_reading_form,
                           edit_form=edit_meter_reading_form,
                           hide_footer=True,
                           title="Readings")


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
        return render_template('accounts/meter_readings.html',
                               form=result['form'],
                               meter_reading=edited_reading,
                               hide_footer=True,
                           title="Edit Reading")


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

    return render_template('accounts/billing.html',
                           make_payment=make_payment_form,
                           billing_data=billing_data,
                           payment_form=make_payment_form,
                           hide_footer=True,
                           title="Billing")


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
            invoice_id=meter_reading.id
        )

        if result['success']:
            flash(result['message'], 'success')
            return redirect(url_for('accounts.records.billing'))
        else:
            flash(result['message'], 'danger')

    return render_template('accounts/billing.html',
                           form=form,
                           meter_reading=meter_reading)


@records_bp.route('/invoice/<int:invoice_id>')
@login_required
def invoice(invoice_id):
    invoice_data = fetch_invoice_data(current_user, invoice_id)
    if invoice_data:
        return render_template('accounts/invoice.html',
                               invoice_data=invoice_data,
                               hide_sidebar=True,
                               hide_navbar=True,
                               hide_footer=True,
                               title="Invoicing")
    else:
        flash("Invoice not found", "error")
        return redirect(url_for('accounts.records.billing'))


@records_bp.route('/payments')
@login_required
def payments():
    payment_data = fetch_payment_data(current_user)
    form = EditPaymentForm()

    return render_template('accounts/payments.html',
                           payment_data=payment_data,
                           form=form,
                           hide_footer=True,
                           title="Payments")


@records_bp.route('/validate_payment/<int:payment_id>', methods=['POST'])
@login_required
def validate_payment(payment_id):
    result = validate_payment_logic(payment_id)

    if result['success']:
        flash(result['message'], 'success')
    else:
        flash(result['message'], 'danger')

    return redirect(url_for('accounts.records.payments'))


@records_bp.route('/edit_payment/<int:payment_id>', methods=['GET', 'POST'])
@login_required
def edit_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    form = EditPaymentForm(obj=payment)

    if form.validate_on_submit():
        form.populate_obj(payment)
        try:
            db.session.commit()
            process_payments_with_context()
            flash('Payment updated successfully!', 'success')
            return redirect(url_for('accounts.records.payments'))
        except Exception as e:
            flash(f'Error updating payment: {str(e)}', 'danger')
    else:
        flash('Invalid form submission for editing payment.', 'danger')

    return render_template('accounts/edit_payment.html',
                           form=form,
                           payment=payment,
                           hide_footer=True)


@records_bp.route('/delete_payment/<int:payment_id>', methods=['GET', 'POST'])
@login_required
def delete_payment(payment_id):
    result = delete_payment_logic(payment_id)

    if result['success']:
        flash(result['message'], 'success')
    else:
        flash(result['message'], 'danger')

    return redirect(url_for('accounts.records.payments'))


@records_bp.route('/download_meter_readings', methods=['GET'])
@login_required
def download_meter_readings_route():
    return download_meter_readings()


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
    return download_invoice(current_user, invoice_id)


def download_invoice(current_user, invoice_id):
    """
    Helper function to download an invoice PDF by its ID.

    Args:
        current_user: The current user object.
        invoice_id (int): The ID of the invoice to be downloaded.

    Returns:
        Response: Flask response containing the invoice PDF file.
    """
    invoice_data = fetch_invoice_data(current_user, invoice_id)
    if invoice_data:
        customer_name = invoice_data.get('customer_name')
        owner_first_name = customer_name.split()[0]

        house_section = invoice_data.get('house_section')
        house_number = invoice_data.get('house_number')
        invoice_id = invoice_data.get('invoice_id')

        date_str = default_datetime().strftime("%d-%b-%Y")

        file_name = f"Invoice_{invoice_id}_{date_str}_{owner_first_name}_{house_section}_house_{house_number}.pdf"

        pdf_data = generate_invoice_pdf(invoice_data)
        return send_file(BytesIO(pdf_data), as_attachment=True, download_name=file_name, mimetype='application/pdf')
    else:
        flash("Invoice not found", "error")
        return redirect(url_for('accounts.records.billing'))


def generate_invoice_pdf(invoice_data):
    """
    Generate PDF file for the invoice.

    Args:
        invoice_data (dict): Data for the invoice.

    Returns:
        bytes: PDF data as bytes.
    """
    html_template = """
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8" />
                        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                        <title>Invoice</title>
                        <style>
                        /* Reset styles */
                        * {
                            box-sizing: border-box;
                            margin: 0;
                            padding: 0;
                        }

                        /* Body styles */
                        body {
                            font-family: Arial, sans-serif;
                            background-color: #f4f4f4;
                            color: #333;
                            line-height: 1.6;
                        }

                        /* Container styles */
                        .container {
                            max-width: 800px;
                            margin: 20px auto;
                            border-radius: 8px;
                            background-color: #fff;
                            padding: 25px;
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        }

                        /* Header styles */
                        header {
                            display: block;
                            align-items: center;
                            margin-bottom: 20px;
                        }

                        header .top-header {
                            display: flex;
                            justify-content: space-between;
                        }

                        header .top-header h1 {
                            font-size: 2em;
                            color: #007bff;
                        }

                        header .bottom-header {
                            display: flex;
                            justify-content: space-between;
                            font-size: 1.1em;
                            color: #555;
                        }

                        /* Section styles */
                        section {
                            margin-bottom: 30px;
                        }

                        h2 {
                            font-size: 1.3em;
                            color: #007bff;
                            margin-bottom: 10px;
                        }

                        ul {
                            list-style-type: none;
                        }

                        /* Table styles */
                        div table {
                            width: 100%;
                            border-collapse: collapse;
                            padding-bottom: 20px;
                        }

                        div th,
                        div td {
                            padding: 3px;
                            border-bottom: none;
                        }

                        div th {
                            text-align: left;
                            background-color: #f8f9fa;
                        }

                        table {
                            width: 100%;
                            border-collapse: collapse;
                        }

                        th,
                        td {
                            padding: 8px;
                            border-bottom: 1px solid #ddd;
                        }

                        th {
                            text-align: left;
                            background-color: #f8f9fa;
                        }

                        /* Footer styles */
                        footer p {
                            font-style: italic;
                            color: #777;
                            text-align: center;
                        }
                        </style>
                    </head>
                    <body>
                        <div class="container">
                        <!-- Invoice Header Section -->
                        <header>
                            <div class="top-header">
                            <h1>Company Name</h1>
                            <h1>Invoice</h1>
                            </div>
                            <div class="bottom-header">
                            <span>Date:</span> {{ invoice_data.timestamp.strftime('%d %b %Y') }}
                            <span>Invoice:</span> #{{ invoice_data.invoice_id }}
                            </div>
                        </header>

                        <!-- Invoice Details Section -->
                        <section>
                            <div>
                            <table style="width: 100%; border: none">
                                <tr>
                                <td style="width: 50%; text-align: left">
                                    <h2>Invoiced To:</h2>
                                    <table>
                                    <tr>
                                        <td><b>Name:</b></td>
                                        <td>
                                        {{ invoice_data.customer_name.title() if
                                        invoice_data.customer_name else 'Bank Name' }}
                                        </td>
                                    </tr>
                                    <tr>
                                        <td><b>Phase:</b></td>
                                        <td>
                                        {{ invoice_data.house_section.title() if
                                        invoice_data.house_section else 'Bank Name' }}
                                        </td>
                                    </tr>
                                    <tr>
                                        <td><b>House No.:</b></td>
                                        <td>
                                        {{ invoice_data.house_number if invoice_data.house_number
                                        else 'Bank Name' }}
                                        </td>
                                    </tr>
                                    <tr>
                                        <td><b>Meter Reading:</b></td>
                                        <td>
                                        {{ invoice_data.reading_value }} Units{% if not
                                        invoice_data.reading_value %}Meter Reading{% endif %}
                                        </td>
                                    </tr>
                                    <tr>
                                        <td><b>Contact No.:</b></td>
                                        <td>
                                        (+254){{ invoice_data.mobile[-9:] if invoice_data.mobile
                                        else 'Bank Name' }}
                                        </td>
                                    </tr>
                                    </table>
                                </td>

                                <td style="width: 50%; text-align: right">
                                    <h2>Pay To:</h2>
                                    <table>
                                    <tr>
                                        <td><b>Name:</b></td>
                                        <td>
                                        {{ company_name.title() if company_name else 'Company
                                        Name' }}
                                        </td>
                                    </tr>
                                    <tr>
                                        <td><b>Gateway:</b></td>
                                        <td>
                                        {{ bank_name.title() if bank_name else 'Bank Name' }}
                                        </td>
                                    </tr>
                                    <tr>
                                        <td><b>Pay Bill No:</b></td>
                                        <td>{{ paybill if paybill else '123456' }}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Account No.:</b></td>
                                        <td>
                                        {{ account_number if account_number else '123456789' }}
                                        </td>
                                    </tr>
                                    <tr>
                                        <td><b>Contact:</b></td>
                                        <td>
                                        {{ contact_number if contact_number else '123456789' }}
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                </tr>
                            </table>
                            </div>
                        </section>

                        <!-- Invoice Items Section -->
                        <section>
                            <table>
                            <thead>
                                <tr>
                                <th>Service</th>
                                <th>Description</th>
                                <th>Rate</th>
                                <th>QTY</th>
                                <th>Amount</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                <td>{{ invoice_data.first_service }}</td>
                                <td>{{ invoice_data.first_description }}</td>
                                <td>KES {{ invoice_data.unit_price | format_amount }}</td>
                                <td>{{ invoice_data.consumed | format_amount }}</td>
                                <td>
                                    KES {{ (invoice_data.unit_price *
                                    invoice_data.consumed) | format_amount }}
                                </td>
                                </tr>
                                <tr>
                                <td>{{ invoice_data.second_service }}</td>
                                <td>{{ invoice_data.second_description }}</td>
                                <td>KES {{ invoice_data.service_fee | format_amount }}</td>
                                <td>{{ invoice_data.service_qty | format_amount }}</td>
                                <td>
                                    KES {{ (invoice_data.service_fee *
                                    invoice_data.service_qty) | format_amount }}
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </section>

                        <!-- Invoice Summary Section -->
                        <section>
                            <div style="display: flex; justify-content: space-between">
                            <div style="width: 48%"></div>
                            <div style="width: 48%">
                                <table>
                                <tbody>
                                    <tr>
                                    <td><b>Sub Total:</b></td>
                                    <td>
                                        KES {{ (invoice_data.sub_total_amount +
                                        invoice_data.service_fee * invoice_data.service_qty) | format_amount }}
                                    </td>
                                    </tr>
                                    <tr>
                                    <td><b>VAT (5%):</b></td>
                                    <td>
                                        KES {{ (0.05 * (invoice_data.sub_total_amount +
                                        invoice_data.service_fee * invoice_data.service_qty)) | format_amount }}
                                    </td>
                                    </tr>
                                    <tr>
                                    <td><b>Total:</b></td>
                                    <td>
                                        KES {{ ((invoice_data.sub_total_amount +
                                        invoice_data.service_fee * invoice_data.service_qty) + (0.05
                                        * (invoice_data.sub_total_amount + invoice_data.service_fee *
                                        invoice_data.service_qty))) | format_amount }}
                                    </td>
                                    </tr>
                                </tbody>
                                </table>
                            </div>
                            </div>
                        </section>

                        <!-- Invoice Footer Section -->
                        <footer>
                            <p>
                            NOTE: This is a computer-generated receipt and does not require a
                            physical signature.
                            </p>
                        </footer>
                        </div>
                    </body>
                    </html>
                    """

    html_data = render_template_string(html_template, invoice_data=invoice_data)

    pdf_data = BytesIO()
    pisa.CreatePDF(BytesIO(html_data.encode()), pdf_data)
    return pdf_data.getvalue()
