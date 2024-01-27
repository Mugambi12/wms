from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    # You can add logic here to fetch and display relevant information
    return render_template('home/home.html', hide_sidebar=True)
