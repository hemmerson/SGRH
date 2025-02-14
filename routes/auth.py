import re

from flask import render_template, request, flash, redirect, url_for, current_app
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash

from models.models import Usuario
from routes import auth_bp
from db import db


def is_valid_email(email):
    """Validar formato do email usando regex"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


def is_valid_password(password):
    """
    Validar força da senha:
    - Mínimo 8 caracteres
    - Pelo menos uma letra maiúscula
    - Pelo menos uma letra minúscula
    - Pelo menos um número
    """
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    return True


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Redirecionar se já estiver logado
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        if not username or not password:
            flash('Por favor, preencha todos os campos.', 'danger')
            return redirect(url_for('auth.login'))

        user = Usuario.query.filter_by(nome=username).first()

        if not user or not user.check_password(password):
            flash('Usuário ou senha incorretos. Por favor, tente novamente.', 'danger')
            return redirect(url_for('auth.login'))

        if not user.is_active:
            flash('Esta conta está desativada. Entre em contato com o administrador.', 'warning')
            return redirect(url_for('auth.login'))

        # Realizar login
        login_user(user, remember=remember)

        # Obter próxima página (se existir)
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('dashboard')

        flash(f'Bem-vindo, {user.nome}!', 'success')
        return redirect(next_page)

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Redirecionar se já estiver logado
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validar preenchimento dos campos
        if not all([username, email, password, confirm_password]):
            flash('Por favor, preencha todos os campos.', 'danger')
            return redirect(url_for('auth.register'))

        # Validar tamanho do nome de usuário
        if len(username) < 3 or len(username) > 30:
            flash('O nome de usuário deve ter entre 3 e 30 caracteres.', 'danger')
            return redirect(url_for('auth.register'))

        # Validar formato do email
        if not is_valid_email(email):
            flash('Por favor, insira um email válido.', 'danger')
            return redirect(url_for('auth.register'))

        # Validar força da senha
        if not is_valid_password(password):
            flash('A senha deve ter pelo menos 8 caracteres, uma letra maiúscula, uma minúscula e um número.', 'danger')
            return redirect(url_for('auth.register'))

        # Validar confirmação de senha
        if password != confirm_password:
            flash('As senhas não coincidem!', 'danger')
            return redirect(url_for('auth.register'))

        # Verificar se usuário já existe
        if Usuario.query.filter_by(nome=username).first():
            flash('Este nome de usuário já está em uso.', 'danger')
            return redirect(url_for('auth.register'))

        # Verificar se email já existe
        if Usuario.query.filter_by(email=email).first():
            flash('Este email já está em uso.', 'danger')
            return redirect(url_for('auth.register'))

        # Criar novo usuário
        try:
            new_user = Usuario(
                nome=username,
                email=email,
                senha=password
            )
            db.session.add(new_user)
            db.session.commit()

            flash('Registro realizado com sucesso! Você já pode fazer login.', 'success')
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Erro ao registrar usuário: {str(e)}')
            flash('Ocorreu um erro ao registrar o usuário. Por favor, tente novamente.', 'danger')
            return redirect(url_for('auth.register'))

    return render_template('auth/register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado com sucesso.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')


@auth_bp.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not all([current_password, new_password, confirm_password]):
            flash('Por favor, preencha todos os campos.', 'danger')
            return redirect(url_for('auth.change_password'))

        if not current_user.check_password(current_password):
            flash('Senha atual incorreta.', 'danger')
            return redirect(url_for('auth.change_password'))

        if not is_valid_password(new_password):
            flash('A nova senha deve ter pelo menos 8 caracteres, uma letra maiúscula, uma minúscula e um número.',
                  'danger')
            return redirect(url_for('auth.change_password'))

        if new_password != confirm_password:
            flash('As senhas não coincidem!', 'danger')
            return redirect(url_for('auth.change_password'))

        try:
            current_user.senha = generate_password_hash(new_password)
            db.session.commit()
            flash('Senha alterada com sucesso!', 'success')
            return redirect(url_for('auth.profile'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Erro ao alterar senha: {str(e)}')
            flash('Ocorreu um erro ao alterar a senha. Por favor, tente novamente.', 'danger')
            return redirect(url_for('auth.change_password'))

    return render_template('auth/change_password.html')