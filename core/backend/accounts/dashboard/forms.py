# File: app/backend/accounts/dashboard/forms.py

from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField

class StickyNoteForm(FlaskForm):
    content = IntegerField('Sticky Note')
    submit = SubmitField('Submit')
