# app/backend/accounts/security/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from core import db
from ...database.models import Contact


website_bp = Blueprint('website', __name__, url_prefix='/website')


@website_bp.route('/website')
@login_required
def website():
    inquiries = Contact.query.all()
    return render_template('accounts/website.html',
                           inquiries=inquiries,
                           hide_footer=True,
                           title="Inquiries")


@website_bp.route('/delete_inquiry/<int:inquiry_id>', methods=['POST'])
@login_required
def delete_inquiry(inquiry_id):
    result = delete_inquiry_logic(inquiry_id)

    if result['success']:
        flash(result['message'], 'success')
    else:
        flash(result['message'], 'danger')

    return redirect(url_for('accounts.website.website'))


def delete_inquiry_logic(inquiry_id):
    try:
        inquiry = Contact.query.get(inquiry_id)

        if inquiry:
            db.session.delete(inquiry)
            db.session.commit()
            return {'success': True, 'message': f'Inquiry {inquiry.id} deleted successfully.'}
        else:
            return {'success': False, 'message': f'Inquiry {inquiry.id} not found.'}

    except Exception as e:
        return {'success': False, 'message': f'Error deleting inquiry: {str(e)}'}
