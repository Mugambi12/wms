# File: Download Manager

from flask import redirect, url_for, flash, render_template_string, send_file, request
from flask_login import current_user
import csv
import io
from io import BytesIO
from openpyxl import Workbook
from xhtml2pdf import pisa
from ...database.models import *
from ..records.utils_data import fetch_invoice_data


def download_users():
    """
    Download users in different formats (CSV, Excel, PDF).

    Returns:
        File: Downloadable file in the specified format.
    """
    format_type = request.args.get('format', 'csv')

    if format_type == 'csv':
        csv_data = generate_users_csv()
        return send_file(
            BytesIO(csv_data.encode('utf-8')),
            as_attachment=True,
            download_name='people_list.csv',
            mimetype='text/csv'
        )
    elif format_type == 'excel':
        excel_data = generate_users_excel()
        return send_file(
            BytesIO(excel_data),
            as_attachment=True,
            download_name='people_list.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    elif format_type == 'pdf':
        people_list = User.query.all()
        pdf_data = generate_users_pdf(people_list)
        return send_file(BytesIO(pdf_data), as_attachment=True, download_name='people_list.pdf')
    else:
        return "Unsupported format", 400


def generate_users_csv():
    """
    Generate CSV file for users.

    Returns:
        str: CSV data as a string.
    """
    data = []
    if current_user.is_authenticated and current_user.is_admin:
        users = User.query.all()
    else:
        users = User.query.filter_by(id=current_user.id).all()

    for person in users:
        data.append([
            person.id,
            f"{person.first_name} {person.last_name}",
            person.email,
            person.mobile_number,
            person.house_section,
            person.house_number,
            'Active' if person.is_active else 'Inactive'
        ])

    csv_buffer = io.StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerow(['', 'ID', 'Name', 'Email', 'Mobile Number', 'House Section', 'House Number', 'Status'])
    csv_writer.writerows(data)

    csv_data = csv_buffer.getvalue()
    csv_buffer.close()

    return csv_data


def generate_users_excel():
    """
    Generate Excel file for users.

    Returns:
        bytes: Excel data as bytes.
    """
    wb = Workbook()
    ws = wb.active
    ws.append(['ID', 'Name', 'Email', 'Mobile Number', 'House Section', 'House Number', 'Status'])

    if current_user.is_authenticated and current_user.is_admin:
        users = User.query.all()
    else:
        users = User.query.filter_by(id=current_user.id).all()

    for person in users:
        ws.append([
            person.id,
            f"{person.first_name} {person.last_name}",
            person.email,
            person.mobile_number,
            person.house_section,
            person.house_number,
            'Active' if person.is_active else 'Inactive'
        ])

    output = BytesIO()
    wb.save(output)
    return output.getvalue()


def generate_users_pdf(people_list):
    """
    Generate PDF file for users.

    Args:
        people_list (list): List of User objects.

    Returns:
        bytes: PDF data as bytes.
    """
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>People List</title>
    </head>

    <body class="container mt-5">
        <h1 class="text-center mb-4">People List</h1>

        <table class="table table-bordered">
        <thead class="table-primary">
              <tr>
                <th scope="col">#</th>
                <th scope="col">ID</th>
                <th scope="col">Name</th>
                <th scope="col">Mobile</th>
                <th scope="col">Email</th>
                <th scope="col">Section</th>
                <th scope="col">House #</th>
                <th scope="col">Status</th>
              </tr>
        </thead>
        <tbody>
            {% for person in people_list %}
            <tr>
                <th scope="row">{{ loop.index }}</th>
                <td>{{ person.id }}</td>
                <td class="text-start">
                  {{ person.first_name.title() ~ " " ~ person.last_name.title() }}
                </td>
                <td>{{ person.mobile_number }}</td>
                <td>{{ person.email }}</td>
                <td>{{ person.house_section }}</td>
                <td>{{ person.house_number }}</td>
                <td>
                  {% if person.is_active %}<span class="text-success">Active</span>
                  {% else %}<span class="text-danger">Inactive</span>{% endif %}
                </td>
            </tr>
            {% endfor %}
        </tbody>
        </table>
    </body>
    </html>
    """

    html_data = render_template_string(html_template, people_list=people_list)

    pdf_data = BytesIO()
    pisa.CreatePDF(BytesIO(html_data.encode()), pdf_data)
    return pdf_data.getvalue()


def download_meter_readings():
    """
    Download meter readings in different formats (CSV, Excel, PDF).

    Returns:
        File: Downloadable file in the specified format.
    """
    format_type = request.args.get('format', 'csv')

    if format_type == 'csv':
        csv_data = generate_meter_readings_csv()
        return send_file(
            BytesIO(csv_data.encode('utf-8')),
            as_attachment=True,
            download_name='all_invoices.csv',
            mimetype='text/csv'
        )
    elif format_type == 'excel':
        excel_data = generate_meter_readings_excel()
        return send_file(
            BytesIO(excel_data),
            as_attachment=True,
            download_name='all_invoices.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    elif format_type == 'pdf':
        readings_list = MeterReading.query.all()
        pdf_data = generate_meter_readings_pdf(readings_list)
        return send_file(BytesIO(pdf_data), as_attachment=True, download_name='all_invoices.pdf')
    else:
        return "Unsupported format", 400


def generate_meter_readings_csv():
    """
    Generate CSV file for meter readings.

    Returns:
        str: CSV data as a string.
    """
    data = []
    if current_user.is_authenticated and current_user.is_admin:
        readings = MeterReading.query.all()
    else:
        readings = MeterReading.query.filter_by(user_id=current_user.id).all()

    for reading in readings:
        data.append([
            reading.id,
            reading.timestamp,
            reading.customer_name,
            reading.house_section,
            reading.house_number,
            reading.reading_value,
            reading.consumed,
            reading.unit_price,
            reading.service_fee,
            reading.sub_total_amount,
            reading.total_amount,
            'Completed' if reading.payment_status else 'Pending'
        ])

    csv_buffer = io.StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerow(['', 'ID', 'Timestamp', 'Customer Name', 'House Section', 'House Number', 'Reading Value', 'Consumed', 'Unit Price', 'Service Fee', 'Sub Total Price', 'Total Price', 'Status'])
    csv_writer.writerows(data)

    csv_data = csv_buffer.getvalue()
    csv_buffer.close()

    return csv_data


def generate_meter_readings_excel():
    """
    Generate Excel file for meter readings.

    Returns:
        bytes: Excel data as bytes.
    """
    wb = Workbook()
    ws = wb.active
    ws.append(['ID', 'Timestamp', 'Customer Name', 'House Section', 'House Number', 'Reading Value', 'Consumed', 'Unit Price', 'Service Fee', 'Sub Total Price', 'Total Price', 'Status'])

    if current_user.is_authenticated and current_user.is_admin:
        readings = MeterReading.query.all()
    else:
        readings = MeterReading.query.filter_by(user_id=current_user.id).all()

    for reading in readings:
        ws.append([
            reading.id,
            reading.timestamp,
            reading.customer_name,
            reading.house_section,
            reading.house_number,
            reading.reading_value,
            reading.consumed,
            reading.unit_price,
            reading.service_fee,
            reading.sub_total_amount,
            reading.total_amount,
            'Completed' if reading.payment_status else 'Pending'
        ])

    output = BytesIO()
    wb.save(output)
    return output.getvalue()


def generate_meter_readings_pdf(readings_list):
    """
    Generate PDF file for meter readings.

    Args:
        readings_list (list): List of MeterReading objects.

    Returns:
        bytes: PDF data as bytes.
    """
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Meter Readings List</title>
    </head>

    <body class="container mt-5">
        <h1 class="text-center mb-4">Meter Readings List</h1>

        <table class="table table-bordered">
        <thead class="table-primary">
              <tr>
                <th scope="col">#</th>
                <th scope="col">ID</th>
                <th scope="col">Timestamp</th>
                <th scope="col">Customer Name</th>
                <th scope="col">House Section</th>
                <th scope="col">House Number</th>
                <th scope="col">Reading Value</th>
                <th scope="col">Consumed</th>
                <th scope="col">Unit Price</th>
                <th scope="col">Service Fee</th>
                <th scope="col">Sub Total Price</th>
                <th scope="col">Total Price</th>
                <th scope="col">Status</th>
              </tr>
        </thead>
        <tbody>
            {% for reading in readings_list %}
            <tr>
                <th scope="row">{{ loop.index }}</th>
                <td>{{ reading.id }}</td>
                <td>{{ reading.timestamp }}</td>
                <td>{{ reading.customer_name }}</td>
                <td>{{ reading.house_section }}</td>
                <td>{{ reading.house_number }}</td>
                <td>{{ reading.reading_value }}</td>
                <td>{{ reading.consumed }}</td>
                <td>{{ reading.unit_price }}</td>
                <td>{{ reading.service_fee }}</td>
                <td>{{ reading.sub_total_amount }}</td>
                <td>{{ reading.total_amount }}</td>
                <td>{{ 'Completed' if reading.payment_status else 'Pending' }}</td>
            </tr>
            {% endfor %}
        </tbody>
        </table>
    </body>
    </html>
    """

    if current_user.is_authenticated and not current_user.is_admin:
        readings_list = [reading for reading in readings_list if reading.user_id == current_user.id]

    html_data = render_template_string(html_template, readings_list=readings_list)

    pdf_data = BytesIO()
    pisa.CreatePDF(BytesIO(html_data.encode()), pdf_data)
    return pdf_data.getvalue()


def download_invoice(invoice_id):
    """
    Helper function to download an invoice PDF by its ID.

    Args:
        invoice_id (int): The ID of the invoice to be downloaded.

    Returns:
        Response: Flask response containing the invoice PDF file.

    """
    invoice_data = fetch_invoice_data(invoice_id)
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
