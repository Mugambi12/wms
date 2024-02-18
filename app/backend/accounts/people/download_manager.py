# File: app/backend/accounts/people/download_manager.py

from io import BytesIO
import pandas as pd
from flask import render_template_string
from openpyxl import Workbook
from xhtml2pdf import pisa
from ...database.models import User


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
                <th scope="col">#</th>
                <th scope="col">ID</th>
                <th scope="col">Name</th>
                <th scope="col">Mobile</th>
                <th scope="col">Email</th>
                <th scope="col">Section</th>
                <th scope="col">House #</th>
                <th scope="col">Balance</th>
                <th scope="col">Status</th>
                <th scope="col">Type</th>
              </tr>
        </thead>
        <tbody>
            {% for person in people_list %}
            <tr>
                <th scope="row">{{ person.id }}</th>
                <td>{{ person.unique_user_id }}</td>
                <td class="text-start">
                  {{ person.first_name.title() ~ " " ~ person.last_name.title()
                  }}
                </td>
                <td>{{ person.mobile_number }}</td>
                <td>{{ person.email }}</td>
                <td>{{ person.house_section }}</td>
                <td>{{ person.house_number }}</td>
                <td
                  class="fw-bold text-center {% if person.balance > 0 %}text-success{% elif person.balance == 0 %}text-dark{% else %}text-danger{% endif %}"
                >
                  {{ "%0.0f"|format(person.balance) }}
                </td>
                <td>
                  {% if person.is_active %}<span class="text-success"
                    >Active</span
                  >{% else %}<span class="text-danger">Inactive</span>{% endif
                  %}
                </td>
                <td>
                  {% if person.is_admin %}<span class="text-success">Admin</span
                  >{% else %}<span class="text-info">Regular</span>{% endif %}
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
