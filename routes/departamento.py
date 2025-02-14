from flask import url_for

from db import db
from models.models import Departamento
from routes import departamento_bp
from routes.generic_router_handler import GenericRouteHandler


def get_departamento_config(registro=None):
    return {
        'list_config': {
            'title': 'Lista de Departamentos',
            'novo_registro_texto': 'Novo Departamento',
            'mensagem_confirmacao': 'Tem certeza que deseja excluir este departamento?',
            'mensagem_lista_vazia': 'Nenhum departamento cadastrado ainda.',
            'colunas': [
                {'campo': 'nome', 'label': 'Nome do Departamento'},
                {
                    'campo': 'profissoes',
                    'label': 'Quantidade de Cargos',
                    'formato': 'custom',
                    'custom_value': lambda obj: len(obj.profissoes)
                }
            ],
            'acoes': True
        },
        'form_config': {
            'titulo': 'Departamento',
            'registro': registro,
            'voltar_url': url_for('departamento.listar'),
            'campos': [
                {
                    'tipo': 'text',
                    'nome': 'nome',
                    'label': 'Nome',
                    'required': True
                }
            ]
        }
    }

# Initialize the generic routes
departamento_routes = GenericRouteHandler(
    model=Departamento,
    db=db,
    blueprint=departamento_bp,
    name='departamento',
    config_function=get_departamento_config
)