# app/backend/accounts/expenses/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Optional

class AddExpenseForm(FlaskForm):
    expense_type = SelectField('Expense Type', choices=[
        ('equipmentAcquisition', 'Equipment Acquisition'),
        ('infrastructureRepairs', 'Infrastructure Repairs'),
        ('maintenance', 'Maintenance Services'),
        ('trainingAndCertifications', 'Training and Certifications'),
        ('utilities', 'Utilities (e.g., electricity)'),
        ('waterQualityTesting', 'Water Quality Testing'),
        ('waterTreatmentChemicals', 'Water Treatment Chemicals')
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
