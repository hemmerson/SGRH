from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import db
from models.models import FolhaPagamento, Pessoa
from routes import folha_pagamento_bp


@folha_pagamento_bp.route('/folhas-pagamento')
def listar():
    folhas = FolhaPagamento.query.all()
    config = {
        'title': 'Lista de Folhas de Pagamento',
        'registros': folhas,
        'novo_registro_url': url_for('folha_pagamento.cadastrar'),
        'novo_registro_texto': 'Nova Folha de Pagamento',
        'editar_url': url_for('folha_pagamento.editar', id=0)[:-1] + '%s',
        'excluir_url': url_for('folha_pagamento.excluir', id=0)[:-1] + '%s',
        'mensagem_confirmacao': 'Tem certeza que deseja excluir esta folha de pagamento?',
        'mensagem_lista_vazia': 'Nenhuma folha de pagamento cadastrada ainda.',
        'colunas': [
            {'campo': 'mes_referencia', 'label': 'Mês/Ano'},
            {'campo': 'data_pagamento', 'label': 'Data de Pagamento', 'formato': 'data'},
            {'campo': 'salario_bruto', 'label': 'Salário Bruto', 'formato': 'moeda'},
            {'campo': 'descontos', 'label': 'Descontos', 'formato': 'moeda'},
            {'campo': 'beneficios', 'label': 'Benefícios', 'formato': 'moeda'},
            {'campo': 'salario_liquido', 'label': 'Salário Líquido', 'formato': 'moeda'},
            {
                'campo': 'pessoas',
                'label': 'Funcionários',
                'formato': 'custom',
                'custom_value': lambda obj: len(obj.pessoas)
            }
        ],
        'acoes': True
    }
    return render_template('components/generic_list.html', **config)


# Rota para adicionar uma nova folha de pagamento
@folha_pagamento_bp.route('/folhas_pagamento/nova', methods=['GET', 'POST'])
def cadastrar():
    pessoas = Pessoa.query.all()

    if request.method == 'POST':
        data_pagamento = request.form['data_pagamento']
        valor_bruto = request.form['valor_bruto']
        descontos = request.form['descontos']
        valor_liquido = float(valor_bruto) - float(descontos)
        mes_referencia = request.form['mes_referencia']

        if not data_pagamento or not valor_bruto or not descontos or not mes_referencia:
            flash("Todos os campos obrigatórios devem ser preenchidos!", "danger")
            return redirect(url_for('folha_pagamento.adicionar_folha_pagamento'))

        nova_folha = FolhaPagamento(
            data_pagamento=data_pagamento,
            valor_bruto=valor_bruto,
            descontos=descontos,
            valor_liquido=valor_liquido,
            mes_referencia=mes_referencia
        )

        db.session.add(nova_folha)
        db.session.commit()
        flash("Folha de pagamento adicionada com sucesso!", "success")
        return redirect(url_for('folha_pagamento.listar_folhas_pagamento'))

    return render_template('folha_pagamento/form.html', pessoas=pessoas)


# Rota para editar uma folha de pagamento
@folha_pagamento_bp.route('/folhas_pagamento/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    folha = FolhaPagamento.query.get_or_404(id)

    if request.method == 'POST':
        folha.data_pagamento = request.form['data_pagamento']
        folha.valor_bruto = request.form['valor_bruto']
        folha.descontos = request.form['descontos']
        folha.valor_liquido = float(folha.valor_bruto) - float(folha.descontos)
        folha.mes_referencia = request.form['mes_referencia']

        db.session.commit()
        flash("Folha de pagamento atualizada com sucesso!", "success")
        return redirect(url_for('folha_pagamento.listar_folhas_pagamento'))

    return render_template('folha_pagamento/form.html', folha=folha)


# Rota para deletar uma folha de pagamento
@folha_pagamento_bp.route('/folhas_pagamento/deletar/<int:id>', methods=['POST'])
def excluir(id):
    folha = FolhaPagamento.query.get_or_404(id)
    db.session.delete(folha)
    db.session.commit()
    flash("Folha de pagamento removida com sucesso!", "success")
    return redirect(url_for('folha_pagamento.listar_folhas_pagamento'))
