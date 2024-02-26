# app/backend/landing/routes.py
from flask import Blueprint, render_template

landing_bp = Blueprint('landing', __name__)

@landing_bp.route('/')
def landing():
    return render_template('landing/landing.html', hide_sidebar=True)
