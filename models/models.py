import re

from sqlalchemy.orm import validates

from db import db

# Tabela de associação para o relacionamento N-N entre Pessoa e FolhaPagamento
pessoa_folha_pagamento = db.Table('pessoa_folha_pagamento',
                                  db.Column('pessoa_id', db.Integer, db.ForeignKey('pessoa.id'), primary_key=True),
                                  db.Column('folha_pagamento_id', db.Integer, db.ForeignKey('folha_pagamento.id'),
                                            primary_key=True)
                                  )


class Pessoa(db.Model):
    __tablename__ = 'pessoa'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    data_admissao = db.Column(db.Date, nullable=False)

    # Relacionamento correto para Profissão (uma pessoa pode ter uma profissão)
    profissao_id = db.Column(db.Integer, db.ForeignKey('profissao.id'))
    profissao = db.relationship('Profissao', backref='pessoas')

    # Relacionamento para Capacitação (um-para-muitos)
    capacitacoes = db.relationship('Capacitacao', backref='pessoa', lazy=True)

    # Relacionamento para Folha de Pagamento (muitos-para-muitos)
    folhas_pagamento = db.relationship('FolhaPagamento',
                                       secondary=pessoa_folha_pagamento,
                                       backref=db.backref('pessoas'))

    def __repr__(self):
        return f'<Pessoa {self.nome}>'

class Departamento(db.Model):
    __tablename__ = 'departamento'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    profissoes = db.relationship('Profissao', backref='departamento', lazy=True)


class Profissao(db.Model):
    __tablename__ = 'profissao'

    id = db.Column(db.Integer, primary_key=True)
    nome_cargo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    salario_base = db.Column(db.Numeric(10, 2), nullable=False)

    departamento_id = db.Column(db.Integer, db.ForeignKey('departamento.id'), nullable=False)

    def __repr__(self):
        return f'<Profissao {self.nome_cargo}>'


class FolhaPagamento(db.Model):
    __tablename__ = 'folha_pagamento'

    id = db.Column(db.Integer, primary_key=True)
    data_pagamento = db.Column(db.Date, nullable=False)
    salario_bruto = db.Column(db.Numeric(10, 2), nullable=False)
    descontos = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    beneficios = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    salario_liquido = db.Column(db.Numeric(10, 2), nullable=False)
    mes_referencia = db.Column(db.String(7), nullable=False)

    def __repr__(self):
        return f'<FolhaPagamento {self.mes_referencia}>'

    @validates('mes_referencia')
    def validate_mes_referencia(self, key, value):
        # Validação do formato MM/YYYY
        if not re.match(r'^\d{2}/\d{4}$', value):
            raise ValueError("Formato inválido para mês de referência. Use MM/YYYY")
        return value


class Capacitacao(db.Model):
    __tablename__ = 'capacitacao'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    instituicao = db.Column(db.String(100), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=True)
    certificado = db.Column(db.Boolean, default=False)

    # Chave estrangeira para Pessoa
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=False)

    def __repr__(self):
        return f'<Capacitacao {self.descricao}>'

    @validates('data_fim')
    def validate_data_fim(self, key, data_fim):
        if data_fim and data_fim < self.data_inicio:
            raise ValueError("Data de fim deve ser posterior à data de início")
        return data_fim


class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False, unique=True)
    senha = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome}>'
