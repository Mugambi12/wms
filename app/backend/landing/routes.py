# app/backend/landing/routes.py
from flask import Blueprint, render_template

landing_bp = Blueprint('landing', __name__)

@landing_bp.route('/')
def landing():
    # You can add logic here to fetch and display relevant information
    return render_template('landing/landing.html', hide_sidebar=True)
