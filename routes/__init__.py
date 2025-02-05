from flask import Blueprint

# Cria os blueprints
auth_bp = Blueprint('auth', __name__)
pessoas_bp = Blueprint('pessoas', __name__)
profissoes_bp = Blueprint('profissoes', __name__)
capacitacoes_bp = Blueprint('capacitacoes', __name__)
folha_pagamento_bp = Blueprint('folha_pagamento', __name__)

# Importa as rotas
from routes import pessoas, profissoes, capacitacoes, folha_pagamento

# Lista de blueprints para registro
blueprints = [
    auth_bp,
    pessoas_bp,
    profissoes_bp,
    capacitacoes_bp,
    folha_pagamento_bp
]
