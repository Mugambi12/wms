# File: app/backend/accounts/records/invoice_download_manager.py

# Import necessary libraries
from flask import redirect, url_for, flash, send_file,  render_template_string
from io import BytesIO
from xhtml2pdf import pisa
from .utils_billing import fetch_invoice_data


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
        pdf_data = generate_invoice_pdf(invoice_data)
        return send_file(BytesIO(pdf_data), as_attachment=True, download_name='invoice.pdf', mimetype='application/pdf')
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
                            <span>Date:</span> {{ invoice_data.timestamp.strftime('%d-%m-%Y') }}
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
                                <td>KES {{ "%0.0f"|format(invoice_data.unit_price) }}</td>
                                <td>{{ "%0.0f"|format(invoice_data.consumed) }}</td>
                                <td>
                                    KES {{ "%0.0f"|format(invoice_data.unit_price *
                                    invoice_data.consumed) }}
                                </td>
                                </tr>
                                <tr>
                                <td>{{ invoice_data.second_service }}</td>
                                <td>{{ invoice_data.second_description }}</td>
                                <td>KES {{ "%0.0f"|format(invoice_data.service_fee) }}</td>
                                <td>{{ "%0.0f"|format(invoice_data.service_qty) }}</td>
                                <td>
                                    KES {{ "%0.0f"|format(invoice_data.service_fee *
                                    invoice_data.service_qty) }}
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
                                        KES {{ "%0.0f"|format(invoice_data.sub_total_price +
                                        invoice_data.service_fee * invoice_data.service_qty) }}
                                    </td>
                                    </tr>
                                    <tr>
                                    <td><b>VAT (5%):</b></td>
                                    <td>
                                        KES {{ "%0.0f"|format(0.05 * (invoice_data.sub_total_price +
                                        invoice_data.service_fee * invoice_data.service_qty)) }}
                                    </td>
                                    </tr>
                                    <tr>
                                    <td><b>Total:</b></td>
                                    <td>
                                        KES {{ "%0.0f"|format((invoice_data.sub_total_price +
                                        invoice_data.service_fee * invoice_data.service_qty) + (0.05
                                        * (invoice_data.sub_total_price + invoice_data.service_fee *
                                        invoice_data.service_qty))) }}
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

