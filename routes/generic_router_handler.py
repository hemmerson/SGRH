from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from sqlalchemy.exc import SQLAlchemyError
from functools import wraps

from utils import process_form_data


class GenericRouteHandler:
    def __init__(self, model, db, blueprint, name, config_function, validators=None):
        """
        Initialize the generic route handler

        Args:
            model: SQLAlchemy model class
            db: SQLAlchemy database instance
            blueprint: Flask blueprint instance
            name: Name used in URLs and messages (e.g., 'profissao')
            config_function: Function that returns form configuration
            validators: List of validator functions to run before save
        """
        self.model = model
        self.db = db
        self.blueprint = blueprint
        self.name = name
        self.get_config = config_function
        self.validators = validators or []

        # Define as funções de view
        self.define_view_functions()

    def define_view_functions(self):
        """Define all view functions and register them with the blueprint"""

        # Registra a rota de listagem
        @self.blueprint.route(f'/{self.name}s')
        @login_required
        def listar():
            return self._listar()

        # Registra a rota de cadastro
        @self.blueprint.route(f'/{self.name}s/novo', methods=['GET', 'POST'])
        @login_required
        def cadastrar():
            return self._cadastrar()

        # Registra a rota de edição
        @self.blueprint.route(f'/{self.name}s/editar/<int:id>', methods=['GET', 'POST'])
        @login_required
        def editar(id):
            return self._editar(id)

        # Registra a rota de exclusão
        @self.blueprint.route(f'/{self.name}s/excluir/<int:id>', methods=['POST'])
        @login_required
        def excluir(id):
            return self._excluir(id)

    def handle_db_operation(self, operation):
        """
        Decorator para manipular operações de banco de dados e erros
        """

        @wraps(operation)
        def wrapper(*args, **kwargs):
            try:
                result = operation(*args, **kwargs)
                self.db.session.commit()
                return result
            except ValueError as e:
                self.db.session.rollback()
                flash(str(e), 'danger')
            except SQLAlchemyError as e:
                self.db.session.rollback()
                flash(f'Erro ao manipular {self.name}. {str(e)}', 'danger')
            return redirect(url_for(f'{self.name}.listar'))

        return wrapper

    def validate_data(self, dados):
        """Executa todos os validadores nos dados"""
        for validator in self.validators:
            validator(dados)

    def _listar(self):
        """Lista todos os registros"""
        registros = self.model.query.all()
        config = self.get_config()['list_config']
        config.update({
            'registros': registros,
            'novo_registro_url': url_for(f'{self.name}.cadastrar'),
            'editar_url': url_for(f'{self.name}.editar', id=0)[:-1] + '%s',
            'excluir_url': url_for(f'{self.name}.excluir', id=0)[:-1] + '%s',
        })
        return render_template('components/generic_list.html', **config)

    def _cadastrar(self):
        """Cria um novo registro"""
        config = self.get_config()['form_config']

        if request.method == 'POST':
            dados = process_form_data(request.form, config['campos'])

            try:
                self.validate_data(dados)

                @self.handle_db_operation
                def create():
                    novo_registro = self.model(**dados)
                    self.db.session.add(novo_registro)
                    flash(f'{self.name.title()} cadastrado com sucesso!', 'success')
                    return redirect(url_for(f'{self.name}.listar'))

                return create()
            except ValueError as e:
                flash(str(e), 'danger')

        return render_template('components/generic_form.html', **config)

    def _editar(self, id):
        """Edita um registro existente"""
        registro = self.model.query.get_or_404(id)
        config = self.get_config(registro)['form_config']

        if request.method == 'POST':
            dados = process_form_data(request.form, config['campos'])

            try:
                self.validate_data(dados)

                @self.handle_db_operation
                def update():
                    for key, value in dados.items():
                        setattr(registro, key, value)
                    flash(f'{self.name.title()} atualizado com sucesso!', 'success')
                    return redirect(url_for(f'{self.name}.listar'))

                return update()
            except ValueError as e:
                flash(str(e), 'danger')

        return render_template('components/generic_form.html', **config)

    def _excluir(self, id):
        """Exclui um registro"""
        registro = self.model.query.get_or_404(id)

        @self.handle_db_operation
        def delete():
            self.db.session.delete(registro)
            flash(f'{self.name.title()} excluído com sucesso!', 'success')
            return redirect(url_for(f'{self.name}.listar'))

        return delete()