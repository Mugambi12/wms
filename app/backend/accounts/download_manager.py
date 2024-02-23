import csv
import io
from flask import render_template_string, send_file, request
from io import BytesIO
from openpyxl import Workbook
from xhtml2pdf import pisa
from ..database.models import User, MeterReading

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
    for person in User.query.all():
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

    for person in User.query.all():
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
        <!-- Bootstrap CSS -->
        <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
        rel="stylesheet"
        />
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
                <th scope="row">{{ person.id }}</th>
                <td>{{ person.unique_user_id }}</td>
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

        <!-- Bootstrap JS and Popper.js -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
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
            download_name='meter_readings.csv',
            mimetype='text/csv'
        )
    elif format_type == 'excel':
        excel_data = generate_meter_readings_excel()
        return send_file(
            BytesIO(excel_data),
            as_attachment=True,
            download_name='meter_readings.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    elif format_type == 'pdf':
        readings_list = MeterReading.query.all()
        pdf_data = generate_meter_readings_pdf(readings_list)
        return send_file(BytesIO(pdf_data), as_attachment=True, download_name='meter_readings.pdf')
    else:
        return "Unsupported format", 400

def generate_meter_readings_csv():
    """
    Generate CSV file for meter readings.

    Returns:
        str: CSV data as a string.
    """
    data = []
    for reading in MeterReading.query.all():
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
            reading.sub_total_price,
            reading.total_price,
            'Completed' if reading.reading_status else 'Pending'
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

    for reading in MeterReading.query.all():
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
            reading.sub_total_price,
            reading.total_price,
            'Completed' if reading.reading_status else 'Pending'
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
        <!-- Bootstrap CSS -->
        <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
        rel="stylesheet"
        />
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
                <td>{{ reading.sub_total_price }}</td>
                <td>{{ reading.total_price }}</td>
                <td>{{ 'Completed' if reading.reading_status else 'Pending' }}</td>
            </tr>
            {% endfor %}
        </tbody>
        </table>

        <!-- Bootstrap JS and Popper.js -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """

    html_data = render_template_string(html_template, readings_list=readings_list)

    pdf_data = BytesIO()
    pisa.CreatePDF(BytesIO(html_data.encode()), pdf_data)
    return pdf_data.getvalue()
