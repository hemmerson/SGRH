from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from app import db
from models.models import FolhaPagamento, Profissao
from routes import folha_pagamento_bp

@folha_pagamento_bp.route('/folha-pagamento')
def listar():
    folhas = FolhaPagamento.query.all()
    return render_template('folha_pagamento/listar.html', folhas=folhas)

@folha_pagamento_bp.route('/folha-pagamento/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    profissoes = Profissao.query.all()
    if request.method == 'POST':
        try:
            folha = FolhaPagamento(
                data_pagamento=datetime.strptime(request.form['data_pagamento'], '%Y-%m-%d'),
                valor_bruto=float(request.form['valor_bruto']),
                descontos=float(request.form['descontos']),
                valor_liquido=float(request.form['valor_bruto']) - float(request.form['descontos']),
                mes_referencia=datetime.strptime(request.form['mes_referencia'], '%Y-%m-%d'),
                profissao_id=int(request.form['profissao_id'])
            )
            db.session.add(folha)
            db.session.commit()
            flash('Folha de pagamento cadastrada com sucesso!', 'success')
            return redirect(url_for('folha_pagamento.listar'))
        except Exception as e:
            flash('Erro ao cadastrar folha de pagamento.', 'danger')
            db.session.rollback()

    return render_template('folha_pagamento/form.html', profissoes=profissoes)

@folha_pagamento_bp.route('/folha-pagamento/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    profissoes = Profissao.query.all()
    folha = FolhaPagamento.query.get_or_404(id)

    if request.method == 'POST':
        try:
            folha.data_pagamento = datetime.strptime(request.form['data_pagamento'], '%Y-%m-%d')
            folha.valor_bruto = float(request.form['valor_bruto'])
            folha.descontos = float(request.form['descontos'])
            folha.valor_liquido = float(request.form['valor_bruto']) - float(request.form['descontos'])
            folha.mes_referencia = datetime.strptime(request.form['mes_referencia'], '%Y-%m-%d')
            folha.profissao_id = int(request.form['profissao_id'])

            db.session.commit()
            flash('Folha de pagamento atualizada com sucesso!', 'success')
            return redirect(url_for('folha_pagamento.listar'))
        except Exception as e:
            flash('Erro ao atualizar folha de pagamento.', 'danger')
            db.session.rollback()

    return render_template('folha_pagamento/form.html', folha=folha, profissoes=profissoes)

@folha_pagamento_bp.route('/folha-pagamento/excluir/<int:id>', methods=['POST'])
def excluir(id):
    folha = FolhaPagamento.query.get_or_404(id)
    try:
        db.session.delete(folha)
        db.session.commit()
        flash('Folha de pagamento excluída com sucesso!', 'success')
    except Exception as e:
        flash('Erro ao excluir folha de pagamento.', 'danger')
        db.session.rollback()

    return redirect(url_for('folha_pagamento.listar'))