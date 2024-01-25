from flask import Blueprint, render_template, redirect, url_for

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login')
def login():
    return render_template('auth/login.html', hide_navbar=True, hide_sidebar=True, hide_footer=True)

@auth_bp.route('/logout')
def logout():
    # Add logout logic here if needed
    return redirect(url_for('auth.login'))

@auth_bp.route('/register')
def register():
    return render_template('auth/register.html', hide_navbar=True, hide_sidebar=True, hide_footer=True)

