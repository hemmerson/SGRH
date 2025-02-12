from flask import Blueprint, render_template

from routes import auth_bp


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('auth/register.html')