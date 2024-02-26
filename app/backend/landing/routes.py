# app/backend/landing/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash


landing_bp = Blueprint('landing', __name__)


@landing_bp.route('/')
def landing():
    form = ContactForm()
    return render_template('landing/landing.html',
                           form=form,
                           hide_sidebar=True)



from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, Email

class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[InputRequired()])
    email = StringField('Email Address', validators=[InputRequired(), Email()])
    message = TextAreaField('Your Message', validators=[InputRequired()])


from app import db
from ..database.models import Contact

from flask import jsonify, flash

@landing_bp.route('/submit_message', methods=['POST'])
def submit_message():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data

        new_contact = Contact(name=name, email=email, message=message)
        db.session.add(new_contact)
        db.session.commit()

        return jsonify({"message": f"{name.title()}, your message has been received. Thank you!"})
    return jsonify({"error": "Validation failed"}), 400
