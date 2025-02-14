import re
from flask_login import UserMixin
from decimal import Decimal

from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash

from db import db

# Tabela intermediária para associar pessoas a uma folha de pagamento
class PessoaFolhaPagamento(db.Model):
    __tablename__ = 'pessoa_folha_pagamento'

    id = db.Column(db.Integer, primary_key=True)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=False)
    folha_pagamento_id = db.Column(db.Integer, db.ForeignKey('folha_pagamento.id'), nullable=False)
    salario_base = db.Column(db.Numeric(10, 2), nullable=False)
    descontos = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    beneficios = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    salario_liquido = db.Column(db.Numeric(10, 2), nullable=False)

    pessoa = db.relationship('Pessoa', backref='folhas_pagamento_pessoa')
    folha_pagamento = db.relationship('FolhaPagamento', backref='folhas_pagamento_pessoa')

    def __repr__(self):
        return f'<PessoaFolhaPagamento {self.pessoa.nome} - {self.folha_pagamento.mes_referencia}>'

    @validates('salario_liquido')
    def validate_salario_liquido(self, key, value):
        if value != (self.salario_base + Decimal(self.beneficios) - Decimal(self.descontos)):
            raise ValueError("Salário líquido não corresponde ao cálculo correto.")
        return value


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
    mes_referencia = db.Column(db.String(7), nullable=False)

    def __repr__(self):
        return f'<FolhaPagamento {self.mes_referencia}>'

    @validates('mes_referencia')
    def validate_mes_referencia(self, key, value):
        if not re.match(r'^\d{2}/\d{4}$', value):
            raise ValueError("Formato inválido para mês de referência. Use MM/YYYY")
        return value

    def calcular_total_salarios_liquidos(self):
        return sum(item.salario_liquido for item in self.folhas_pagamento_pessoa)


class Capacitacao(db.Model):
    __tablename__ = 'capacitacao'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    instituicao = db.Column(db.String(100), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=True)
    certificado = db.Column(db.Boolean, default=False)

    # Chave estrangeira para Pessoa
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=False)

    def __repr__(self):
        return f'<Capacitacao {self.titulo}>'

    @validates('data_fim')
    def validate_data_fim(self, key, data_fim):
        if data_fim and data_fim < self.data_inicio:
            raise ValueError("Data de fim deve ser posterior à data de início")
        return data_fim


class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = generate_password_hash(senha)

    def check_password(self, senha):
        return check_password_hash(self.senha, senha)

    def __repr__(self):
        return f'<Usuario {self.nome}>'