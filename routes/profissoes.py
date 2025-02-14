from flask import url_for
from models.models import Profissao, Departamento
from routes import profissao_bp
from db import db
from routes.generic_router_handler import GenericRouteHandler

def get_profissao_config(registro=None):
    """Configuration function for Profissao model"""
    return {
        'list_config': {
            'title': 'Lista de Profissões',
            'novo_registro_texto': 'Nova Profissão',
            'mensagem_confirmacao': 'Tem certeza que deseja excluir esta profissão?',
            'mensagem_lista_vazia': 'Nenhuma profissão cadastrada ainda.',
            'colunas': [
                {'campo': 'nome_cargo', 'label': 'Nome do cargo'},
                {'campo': 'descricao', 'label': 'Descrição'},
                {'campo': 'salario_base', 'label': 'Salário Base', 'formato': 'moeda'},
                {
                    'campo': 'departamento',
                    'label': 'Departamento',
                    'formato': 'relacionamento',
                    'campo_relacionamento': 'nome'
                }
            ],
            'acoes': True
        },
        'form_config': {
            'titulo': 'Profissão',
            'registro': registro,
            'voltar_url': url_for('profissao.listar'),
            'campos': [
                {
                    'tipo': 'text',
                    'nome': 'nome_cargo',
                    'label': 'Cargo',
                    'required': True,
                },
                {
                    'tipo': 'textarea',
                    'nome': 'descricao',
                    'label': 'Descrição',
                    'required': True,
                },
                {
                    'tipo': 'number',
                    'nome': 'salario_base',
                    'label': 'Salário Base',
                    'required': True,
                },
                {
                    'tipo': 'select',
                    'nome': 'departamento_id',
                    'label': 'Departamento',
                    'required': True,
                    'opcoes': [
                        {'value': d.id, 'label': d.nome}
                        for d in Departamento.query.all()
                    ]
                }
            ]
        }
    }

# Adiciona validação específica para salário base
def validar_salario(dados):
    try:
        salario = float(dados.get('salario_base', 0))
        if salario <= 0:
            raise ValueError("Salário base deve ser maior que zero!")
    except (ValueError, TypeError):
        raise ValueError("Salário base deve ser um valor numérico válido!")
    return True

# Initialize the generic routes for Profissao with custom validation
profissao_routes = GenericRouteHandler(
    model=Profissao,
    db=db,
    blueprint=profissao_bp,
    name='profissao',
    config_function=get_profissao_config,
    validators=[validar_salario]  # Adiciona validação específica
)