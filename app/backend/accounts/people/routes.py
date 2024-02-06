# app/backend/accounts/people/routes.py
import os
from io import BytesIO
import pandas as pd
from flask import Blueprint, flash, render_template, redirect, url_for, send_file, render_template_string, request, current_app
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from openpyxl import Workbook
from xhtml2pdf import pisa
from app import db
from ...models.user import User, Settings
from .forms import AddUserForm, EditUserForm, EditProfilePictureForm


people_bp = Blueprint('people', __name__, url_prefix='/people')


@people_bp.route('/people_list', methods=['GET', 'POST'])
@login_required
def people_list():
    if current_user.is_authenticated:
        people_list = User.query.all()
        add_form = AddUserForm()

        # Retrieve house sections and populate the choices
        house_sections = []
        settings = Settings.query.first()
        if settings:
            house_sections = [(section, section) for section in settings.house_sections.split(',')]

        return render_template('accounts/people_list.html', people_list=people_list, house_sections=house_sections, form=add_form, hide_footer=True)
    else:
        return redirect(url_for('auth.login'))


@people_bp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if current_user.is_authenticated:
        add_form = AddUserForm()

        if request.method == 'POST':
            form_type = request.form.get('form_type')

            if form_type == 'add':
                result = handle_add_new_users(add_form, current_user)

                if result['success']:
                    flash(result['message'], 'success')
                else:
                    flash(result['message'], 'danger')
        return redirect(url_for('accounts.people.people_list', people_list=people_list, form=add_form, hide_footer=True))
    else:
        return redirect(url_for('auth.login'))


def handle_add_new_users(form):
    mobile_number = form.mobile_number.data
    first_name = form.first_name.data
    last_name = form.last_name.data
    email = form.email.data
    house_section = form.house_section.data
    house_number = form.house_number.data
    password = form.password.data

    try:
        # Check if the mobile number is already registered
        existing_user = User.query.filter_by(mobile_number=mobile_number).first()
        if existing_user:
            return {'success': False, 'message': 'Failed to add user. Mobile number is already registered.'}

        # Check if the household is already registered
        existing_household = User.query.filter_by(house_section=house_section, house_number=house_number).first()
        if existing_household:
            return {'success': False, 'message': 'Failed to add user. Household is already registered.'}

        # Create a new user object
        new_user = User(
            mobile_number=mobile_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            house_section=house_section,
            house_number=house_number,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        return {'success': True, 'message': f'{first_name.title()} has been successfully added as a user.'}

    except Exception as e:
        return {'success': False, 'message': f'Failed to add user. An error occurred: {str(e)}'}




@people_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.is_authenticated:
        user = User.query.get_or_404(user_id)
        form = EditUserForm(request.form, obj=user)

        # Populate house sections choices
        form.populate_house_sections()

        if request.method == 'POST' and form.validate():
            if form.new_password.data:
                if not validate_new_password(form.new_password.data):
                    flash('New password must be at least 6 characters long.', 'danger')
                    return render_template('accounts/edit_people.html', user=user, form=form, hide_footer=True)

            if change_password(user, form):
                form.populate_obj(user)
                db.session.commit()
                flash(f'Successfully updated profile for {user.first_name.title()}.', 'success')
                return redirect(url_for('accounts.people.people_list'))

        return render_template('accounts/edit_people.html', user=user, form=form, hide_footer=True)
    else:
        return redirect(url_for('auth.login'))


def change_password(user, form):
    if current_user.is_admin and form.current_password.data:
        if not user.check_password(form.current_password.data):
            flash('Current password is incorrect.', 'danger')
            return False

        if form.new_password.data:
            user.password_hash = generate_password_hash(form.new_password.data)

    return True

def validate_new_password(password):
    return len(password) >= 6


@people_bp.route('/edit_profile_picture', methods=['GET', 'POST'])
@login_required
def edit_profile_picture():
    if current_user.is_authenticated:
        form = EditProfilePictureForm()

        if request.method == 'POST' and form.validate():
            if form.profile_image.data:
                profile_picture = form.profile_image.data

                filename = secure_filename(f"{current_user.mobile_number}.png")

                uploads_folder = os.path.join(current_app.root_path, 'assets', 'static', 'uploads', 'profile')
                save_path = os.path.join(uploads_folder, filename)

                try:
                    profile_picture.save(save_path)
                    current_user.profile_image = url_for('static', filename=f'uploads/profile/{filename}')
                    db.session.commit()
                    flash('Profile picture updated successfully.', 'success')
                    return redirect(url_for('accounts.people.people_list'))
                except Exception as e:
                    flash(f'Error updating profile picture: {str(e)}', 'danger')

        return render_template('accounts/edit_people.html', form=form)
    else:
        return redirect(url_for('auth.login'))

@people_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.is_authenticated:
        user = User.query.get_or_404(user_id)

        if user == current_user:
            flash('You cannot delete your own account.', 'danger')
            return redirect(url_for('accounts.people.people_list'))

        db.session.delete(user)
        db.session.commit()
        flash(f'Successfully deleted the user {user.first_name.title()}.', 'success')
        return redirect(url_for('accounts.people.people_list'))
    else:
        return redirect(url_for('auth.login'))


# Download Logic Manager
@people_bp.route('/download_users', methods=['GET'])
@login_required
def download_users():
    format_type = request.args.get('format', 'csv')

    if format_type == 'csv':
        csv_data = generate_csv()
        return send_file(
            BytesIO(csv_data.encode('utf-8')),
            as_attachment=True,
            download_name='people_list.csv',
            mimetype='text/csv'
        )
    elif format_type == 'excel':
        excel_data = generate_excel()
        return send_file(
            BytesIO(excel_data),
            as_attachment=True,
            download_name='people_list.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    elif format_type == 'pdf':
        people_list = User.query.all()
        pdf_data = generate_pdf(people_list)

        return send_file(BytesIO(pdf_data), as_attachment=True, download_name='people_list.pdf')
    else:
        return "Unsupported format", 400

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
