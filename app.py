import os
from flask import Flask, render_template
from flask_login import LoginManager

from db import db
from models.models import Pessoa, Profissao, Capacitacao, FolhaPagamento, Departamento, Usuario
from routes import blueprints


def create_app():
    app = Flask(__name__)

    # Configurações
    # Melhor prática: usar variável de ambiente para a chave secreta
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'uma-chave-secreta-padrao')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicialização
    db.init_app(app)

    # Configurar Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'

    # User loader function
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Registro de blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    # Rotas principais
    @app.route('/')
    @app.route('/dashboard')
    def dashboard():
        stats = {
            'total_departamentos': Departamento.query.count(),
            'total_pessoas': Pessoa.query.count(),
            'total_profissoes': Profissao.query.count(),
            'total_capacitacoes': Capacitacao.query.count(),
            'total_folhas': FolhaPagamento.query.count()
        }
        return render_template('index.html', stats=stats)

    # Criar tabelas - Movido para antes do return
    with app.app_context():
        db.create_all()

    return app


# Criar uma instância da aplicação
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)