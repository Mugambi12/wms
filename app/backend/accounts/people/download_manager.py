# app/backend/accounts/people/download_manager.py
from io import BytesIO
import pandas as pd
from flask import render_template_string
from openpyxl import Workbook
from xhtml2pdf import pisa
from ...models.user import User

def generate_csv():
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

    df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Mobile Number', 'House Section', 'House Number', 'Status'])
    return df.to_csv(index=False)

def generate_excel():
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

def generate_pdf(people_list):
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
            <th>ID</th>
            <th>Full Name</th>
            <th>Mobile Number</th>
            <th>Email</th>
            <th>House Section</th>
            <th>House Number</th>
            <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {% for person in people_list %}
            <tr>
            <td>{{ person.id }}</td>
            <td>{{ person.first_name }} {{ person.last_name }}</td>
            <td>{{ person.mobile_number }}</td>
            <td>{{ person.email }}</td>
            <td>{{ person.house_section }}</td>
            <td>{{ person.house_number }}</td>
            <td>{{ 'Active' if person.is_active else 'Inactive' }}</td>
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
