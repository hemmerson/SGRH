from flask import url_for
from models.models import Pessoa, Profissao
from routes import bp_pessoa
from db import db
from routes.generic_router_handler import GenericRouteHandler

def get_pessoa_config(registro=None):
    return {
        'list_config': {
            'title': 'Lista de Pessoas',
            'novo_registro_texto': 'Nova Pessoa',
            'mensagem_confirmacao': 'Tem certeza que deseja excluir esta pessoa?',
            'mensagem_lista_vazia': 'Nenhuma pessoa cadastrada ainda.',
            'colunas': [
                {'campo': 'nome', 'label': 'Nome'},
                {'campo': 'data_nascimento', 'label': 'Data de Nascimento', 'formato': 'data'},
                {'campo': 'telefone', 'label': 'Telefone'},
                {'campo': 'email', 'label': 'E-mail'},
                {'campo': 'data_admissao', 'label': 'Data de Admissão', 'formato': 'data'},
                {
                    'campo': 'profissao',
                    'label': 'Cargo',
                    'formato': 'relacionamento',
                    'campo_relacionamento': 'nome_cargo'
                }
            ],
            'acoes': True
        },
        'form_config': {
            'titulo': 'Pessoa',
            'registro': registro,
            'voltar_url': url_for('pessoa.listar'),
            'campos': [
                {
                    'tipo': 'text',
                    'nome': 'nome',
                    'label': 'Nome Completo',
                    'required': True
                },
                {
                    'tipo': 'date',
                    'nome': 'data_nascimento',
                    'label': 'Data de Nascimento',
                    'required': True
                },
                {
                    'tipo': 'textarea',
                    'nome': 'endereco',
                    'label': 'Endereço',
                    'required': True
                },
                {
                    'tipo': 'text',
                    'nome': 'telefone',
                    'label': 'Telefone',
                    'required': True,
                    'help_text': 'Digite apenas números'
                },
                {
                    'tipo': 'email',
                    'nome': 'email',
                    'label': 'E-mail',
                    'required': True
                },
                {
                    'tipo': 'date',
                    'nome': 'data_admissao',
                    'label': 'Data de Admissão',
                    'required': True
                },
                {
                    'tipo': 'select',
                    'nome': 'profissao_id',
                    'label': 'Cargo',
                    'required': True,
                    'opcoes': [
                        {'value': p.id, 'label': p.nome_cargo}
                        for p in Profissao.query.all()
                    ]
                }
            ]
        }
    }


pessoa_routes = GenericRouteHandler(
    model=Pessoa,
    db=db,
    blueprint=bp_pessoa,
    name='pessoa',
    config_function=get_pessoa_config
)