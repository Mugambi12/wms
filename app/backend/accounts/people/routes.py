# app/backend/accounts/people/routes.py
import os
from io import BytesIO
import pandas as pd
from flask import Blueprint, flash, render_template, redirect, url_for, send_file, render_template_string, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from openpyxl import Workbook
from xhtml2pdf import pisa
from app import db
from ...models.user import User, db
from .forms import EditUserForm, EditProfilePictureForm, AddUserForm


people_bp = Blueprint('people', __name__, url_prefix='/people')


@people_bp.route('/people_list')
@login_required
def people_list():
    if current_user.is_authenticated:
        people_list = User.query.all()

        return render_template('accounts/people_list.html', hide_footer=True, people_list=people_list)
    else:
        return redirect(url_for('auth.login'))


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
    <html>
        <head>
            <title>People List</title>
        </head>
        <body>
            <h1>People List</h1>
            <table border="1">
                <tr>
                    <th>ID</th>
                    <th>Full Name</th>
                    <th>Mobile Number</th>
                    <th>Email</th>
                    <th>House Section</th>
                    <th>House Number</th>
                    <th>Status</th>
                </tr>
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
            </table>
        </body>
    </html>
    """

    html_data = render_template_string(html_template, people_list=people_list)

    pdf_data = BytesIO()
    pisa.CreatePDF(BytesIO(html_data.encode()), pdf_data)
    return pdf_data.getvalue()


@people_bp.route('/add_people', methods=['GET', 'POST'])
@login_required
def add_people():
    form = AddUserForm()

    if request.method == 'POST' and form.validate():
        # Create a new user
        new_user = User(
            mobile_number=form.mobile_number.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            house_section=form.house_section.data,
            house_number=form.house_number.data,
            is_active=form.is_active.data,
            is_admin=form.is_admin.data
        )

        # Commit the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('User added successfully.', 'success')
        return redirect(url_for('accounts.people.people_list'))

    return render_template('accounts/add_people.html', form=form, hide_footer=True)



from werkzeug.security import generate_password_hash, check_password_hash
def change_password(user, form):
    if current_user.is_admin and form.current_password.data:
        if not user.check_password(form.current_password.data):
            flash('Current password is incorrect.', 'danger')
            return False

        # Assuming you have a method to hash and update the password
        user.password_hash = generate_password_hash(form.new_password.data)

    return True


@people_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm(request.form, obj=user)

    if request.method == 'POST' and form.validate():
        if change_password(user, form):
            form.populate_obj(user)
            db.session.commit()
            flash(f'Successfully updated profile for {user.first_name.title()}.', 'success')
            return redirect(url_for('accounts.people.people_list'))

    return render_template('accounts/edit_people.html', user=user, form=form, hide_footer=True)

@people_bp.route('/edit_profile_picture', methods=['GET', 'POST'])
@login_required
def edit_profile_picture():
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
