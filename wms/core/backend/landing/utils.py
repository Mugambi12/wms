from flask import render_template, jsonify
from .form import ContactForm
from core import db
from ..database.models import Contact


def _landing():
    form = ContactForm()
    return render_template('landing/landing.html',
                           form=form,
                           title="Home",
                           hide_sidebar=True)

def _submit_message():
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
