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

    # Relacionamentos
    profissoes = db.relationship('Profissao', backref='pessoa', lazy=True)
    capacitacoes = db.relationship('Capacitacao', backref='pessoa', lazy=True)
    folhas_pagamento = db.relationship('FolhaPagamento',
                                       secondary=pessoa_folha_pagamento,
                                       lazy='subquery',
                                       backref=db.backref('pessoas', lazy=True))

    def __repr__(self):
        return f'<Pessoa {self.nome}>'


class Profissao(db.Model):
    __tablename__ = 'profissao'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    salario_base = db.Column(db.Numeric(10, 2), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)

    # Chave estrangeira para Pessoa
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=False)

    # Relacionamento com FolhaPagamento
    folhas_pagamento = db.relationship('FolhaPagamento', backref='profissao', lazy=True)

    def __repr__(self):
        return f'<Profissao {self.descricao}>'


class FolhaPagamento(db.Model):
    __tablename__ = 'folha_pagamento'

    id = db.Column(db.Integer, primary_key=True)
    data_pagamento = db.Column(db.Date, nullable=False)
    valor_bruto = db.Column(db.Numeric(10, 2), nullable=False)
    descontos = db.Column(db.Numeric(10, 2), nullable=False)
    valor_liquido = db.Column(db.Numeric(10, 2), nullable=False)
    mes_referencia = db.Column(db.Date, nullable=False)

    # Chave estrangeira para Profissao
    profissao_id = db.Column(db.Integer, db.ForeignKey('profissao.id'), nullable=False)

    def __repr__(self):
        return f'<FolhaPagamento {self.mes_referencia}>'


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



class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False, unique=True)
    senha = db.Column(db.String())