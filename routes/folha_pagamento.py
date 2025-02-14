from decimal import Decimal

from flask import render_template, request, redirect, url_for, flash
from datetime import datetime

from flask_login import login_required
from sqlalchemy import func

from db import db
from models.models import FolhaPagamento, Pessoa, PessoaFolhaPagamento
from routes import folha_pagamento_bp

@folha_pagamento_bp.route('/folha_pagamento')
@login_required
def listar_folhas():
    folhas = FolhaPagamento.query.order_by(
        func.substr(FolhaPagamento.mes_referencia, 4, 4).desc(),  # Ano (YYYY)
        func.substr(FolhaPagamento.mes_referencia, 1, 2).desc()  # Mês (MM)
    ).all()
    return render_template('folha/listar.html', folhas=folhas)


@folha_pagamento_bp.route('/folha_pagamento/nova', methods=['GET', 'POST'])
@login_required
def criar_folha():
    if request.method == 'POST':
        mes_referencia = request.form['mes_referencia']
        data_pagamento = datetime.strptime(request.form['data_pagamento'], '%Y-%m-%d')

        nova_folha = FolhaPagamento(mes_referencia=mes_referencia, data_pagamento=data_pagamento)
        db.session.add(nova_folha)
        db.session.commit()
        flash('Folha de pagamento criada com sucesso!', 'success')
        return redirect(url_for('folha_pagamento.listar_folhas'))

    return render_template('folha/criar.html')

@login_required
@folha_pagamento_bp.route('/folha_pagamento/<int:folha_id>', methods=['GET'])
def detalhes_folha(folha_id):
    folha = FolhaPagamento.query.get_or_404(folha_id)
    return render_template('folha/detalhes.html', folha=folha)

@login_required
@folha_pagamento_bp.route('/folha_pagamento/<int:folha_id>/adicionar_pessoa', methods=['GET', 'POST'])
def adicionar_pessoa(folha_id):
    folha = FolhaPagamento.query.get_or_404(folha_id)
    pessoas = Pessoa.query.all()

    if request.method == 'POST':
        pessoa_id = request.form['pessoa_id']
        pessoa = Pessoa.query.get(pessoa_id)
        salario_base = pessoa.profissao.salario_base
        descontos = float(request.form['descontos'])
        beneficios = float(request.form['beneficios'])
        salario_liquido = salario_base + Decimal(beneficios) - Decimal(descontos)

        pessoa_folha = PessoaFolhaPagamento(
            pessoa_id=pessoa_id,
            folha_pagamento_id=folha_id,
            salario_base=salario_base,
            descontos=descontos,
            beneficios=beneficios,
            salario_liquido=salario_liquido
        )

        db.session.add(pessoa_folha)
        db.session.commit()
        flash(f'Pessoa {pessoa.nome} adicionada à folha!', 'success')
        return redirect(url_for('folha_pagamento.detalhes_folha', folha_id=folha_id))

    return render_template('folha/adicionar_pessoa.html', folha=folha, pessoas=pessoas)

@login_required
@folha_pagamento_bp.route('/folha_pagamento/<int:folha_id>/remover_pessoa/<int:pessoa_id>', methods=['POST'])
def remover_pessoa(folha_id, pessoa_id):
    pessoa_folha = PessoaFolhaPagamento.query.filter_by(folha_pagamento_id=folha_id, pessoa_id=pessoa_id).first()

    if pessoa_folha:
        db.session.delete(pessoa_folha)
        db.session.commit()
        flash('Pessoa removida da folha com sucesso!', 'success')

    return redirect(url_for('folha_pagamento.detalhes_folha', folha_id=folha_id))
