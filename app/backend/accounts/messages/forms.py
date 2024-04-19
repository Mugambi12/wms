# File: app/backend/accounts/messages/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length


class MessageForm(FlaskForm):
    receiver_id = HiddenField('Receiver ID', validators=[DataRequired()])
    content = StringField('Message', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Send')
