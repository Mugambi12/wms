from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length

# Define Flask form
class MessageForm(FlaskForm):
    receiver_id = HiddenField('Receiver ID', validators=[DataRequired()])
    content = StringField('Message', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Send')

