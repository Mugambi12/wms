from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    user='silas'
    # You can add logic here to fetch and display relevant information
    return render_template('home/home.html', user=user, hide_sidebar=True)
