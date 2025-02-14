from flask import Blueprint

# Cria os blueprints
auth_bp = Blueprint('auth', __name__)
bp_pessoa = Blueprint('pessoa', __name__)
profissao_bp = Blueprint('profissao', __name__)
capacitacao_bp = Blueprint('capacitacao', __name__)
departamento_bp = Blueprint('departamento', __name__)
folha_pagamento_bp = Blueprint('folha_pagamento', __name__)

# Lista de blueprints para registro
blueprints = [
    auth_bp,
    bp_pessoa,
    profissao_bp,
    capacitacao_bp,
    departamento_bp,
    folha_pagamento_bp
]

# Importa as rotas
from routes import pessoas, profissoes, capacitacoes, folha_pagamento, departamento, auth