# app/backend/accounts/expenses/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Optional

class AddExpenseForm(FlaskForm):
    expense_type = SelectField('Expense Type', choices=[
        ('Equipment Acquisition', 'Equipment Acquisition'),
        ('Infrastructure Repairs', 'Infrastructure Repairs'),
        ('Maintenance Services', 'Maintenance Services'),
        ('Training and Certifications', 'Training and Certifications'),
        ('Utilities', 'Utilities (e.g., electricity)'),
        ('Water Quality Testing', 'Water Quality Testing'),
        ('Water Treatment Chemicals', 'Water Treatment Chemicals')
    ], validators=[DataRequired()])
    vendor = StringField('Vendor', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    status = SelectField('Status', choices=[
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Completed', 'Completed'),
    ('Rejected', 'Rejected')
], validators=[Optional()])
