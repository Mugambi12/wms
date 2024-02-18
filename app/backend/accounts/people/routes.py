# app/backend/accounts/people/routes.py
from io import BytesIO
from flask import Blueprint, flash, render_template, redirect, url_for, send_file, request
from flask_login import login_required, current_user
from app import db
from ...database.models import User, Settings
from .forms import AddUserForm, EditUserForm, EditProfilePictureForm
from .people import handle_add_new_users, change_password, validate_new_password, save_profile_picture, delete_user
from .download_manager import generate_csv, generate_excel, generate_pdf


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
                else:
                    # Change password only if new password is provided
                    change_password(user, form)

            # Update user profile
            form.populate_obj(user)
            db.session.commit()
            flash(f'Successfully updated profile for {user.first_name.title()}.', 'success')
            return redirect(url_for('accounts.people.people_list'))

        return render_template('accounts/edit_people.html', user=user, form=form, hide_footer=True)
    else:
        return redirect(url_for('auth.login'))


@people_bp.route('/edit_profile_picture', methods=['GET', 'POST'])
@login_required
def edit_profile_picture_route():
    if current_user.is_authenticated:
        form = EditProfilePictureForm()

        if request.method == 'POST' and form.validate():
            if form.profile_image.data:
                if save_profile_picture(form.profile_image.data):
                    flash('Profile picture updated successfully.', 'success')
                    return redirect(url_for('accounts.people.people_list'))
                else:
                    flash('Error updating profile picture.', 'danger')

        return render_template('accounts/edit_people.html', form=form)
    else:
        return redirect(url_for('auth.login'))


@people_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user_route(user_id):
    if current_user.is_authenticated:
        user = User.query.get_or_404(user_id)

        if user == current_user:
            flash('You cannot delete your own account.', 'danger')
            return redirect(url_for('accounts.people.people_list'))

        if delete_user(user):
            flash(f'Successfully deleted the user {user.first_name.title()}.', 'success')
        else:
            flash(f'Error deleting the user {user.first_name.title()}.', 'danger')

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
