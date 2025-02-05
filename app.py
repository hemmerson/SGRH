import os
from flask import Flask, render_template
from db import db
from models.models import Usuario, Pessoa, Profissao, Capacitacao, FolhaPagamento
from routes import blueprints


def create_app():
    app = Flask(__name__)

    # Configurações
    app.config['SECRET_KEY'] = os.urandom(24).hex()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicialização
    db.init_app(app)

    # Registro de blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    # Rotas principais
    @app.route('/')
    def index():
        stats = {
            'total_pessoas': Pessoa.query.count(),
            'total_profissoes': Profissao.query.count(),
            'total_capacitacoes': Capacitacao.query.count(),
            'total_folhas': FolhaPagamento.query.count()
        }
        return render_template('index.html', stats=stats)

    # Criar tabelas
    with app.app_context():
        db.create_all()

    return app


# Criar uma instância da aplicação
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)