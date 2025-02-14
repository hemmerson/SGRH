from flask import url_for
from models.models import Capacitacao, Pessoa
from routes import capacitacao_bp
from db import db
from routes.generic_router_handler import GenericRouteHandler


def get_capacitacao_config(registro=None):
    """Configuration function for Capacitacao model"""
    return {
        'list_config': {
            'title': 'Lista de Capacitações',
            'novo_registro_texto': 'Nova Capacitação',
            'mensagem_confirmacao': 'Tem certeza que deseja excluir esta capacitação?',
            'mensagem_lista_vazia': 'Nenhuma capacitação cadastrada ainda.',
            'colunas': [
                {'campo': 'titulo', 'label': 'Titulo'},
                {'campo': 'instituicao', 'label': 'Instituição'},
                {'campo': 'data_inicio', 'label': 'Data Início', 'formato': 'data'},
                {'campo': 'data_fim', 'label': 'Data Fim', 'formato': 'data'},
                {
                    'campo': 'certificado',
                    'label': 'Certificado',
                    'formato': 'booleano',
                    'valores_booleanos': ['Sim', 'Não']
                },
                {
                    'campo': 'pessoa',
                    'label': 'Pessoa',
                    'formato': 'relacionamento',
                    'campo_relacionamento': 'nome'
                }
            ],
            'acoes': True
        },
        'form_config': {
            'titulo': 'Capacitação',
            'registro': registro,
            'voltar_url': url_for('capacitacao.listar'),
            'campos': [
                {
                    'tipo': 'select',
                    'nome': 'pessoa_id',
                    'label': 'Pessoa',
                    'required': True,
                    'opcoes': [
                        {'value': p.id, 'label': p.nome}
                        for p in Pessoa.query.all()
                    ]
                },
                {
                    'tipo': 'text',
                    'nome': 'titulo',
                    'label': 'Título',
                    'required': True
                },
                {
                    'tipo': 'textarea',
                    'nome': 'descricao',
                    'label': 'Descrição',
                    'required': True,
                    'rows': 3
                },
                {
                    'tipo': 'text',
                    'nome': 'instituicao',
                    'label': 'Instituição de Ensino',
                    'required': True
                },
                {
                    'tipo': 'date',
                    'nome': 'data_inicio',
                    'label': 'Data de Início',
                    'required': True
                },
                {
                    'tipo': 'date',
                    'nome': 'data_fim',
                    'label': 'Data de Conclusão'
                },
                {
                    'tipo': 'checkbox',
                    'nome': 'certificado',
                    'label': 'Certificado?',
                    'valor_padrao': True
                }
            ]
        }
    }


def validar_datas(dados):
    """Validação para garantir que a data de fim não seja anterior à data de início"""
    data_inicio = dados.get('data_inicio')
    data_fim = dados.get('data_fim')

    if data_inicio and data_fim and data_fim < data_inicio:
        raise ValueError("A data de conclusão não pode ser anterior à data de início!")
    return True


# Initialize the generic routes for Capacitacao with custom validation
capacitacao_routes = GenericRouteHandler(
    model=Capacitacao,
    db=db,
    blueprint=capacitacao_bp,
    name='capacitacao',
    config_function=get_capacitacao_config,
    validators=[validar_datas]  # Adiciona validação específica para datas
)