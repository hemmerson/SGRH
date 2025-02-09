from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import db
from models.models import Capacitacao, Pessoa
from routes import capacitacao_bp


# Rota para listar capacitações
@capacitacao_bp.route('/capacitacoes')
def listar():
    capacitacoes = Capacitacao.query.all()
    return render_template('capacitacao/listar.html', capacitacoes=capacitacoes)


# Rota para adicionar uma nova capacitação
@capacitacao_bp.route('/capacitacoes/nova', methods=['GET', 'POST'])
def cadastrar():
    pessoas = Pessoa.query.all()

    if request.method == 'POST':
        descricao = request.form['descricao']
        instituicao = request.form['instituicao']
        data_inicio = request.form['data_inicio']
        data_fim = request.form.get('data_fim', None)
        certificado = True if 'certificado' in request.form else False
        pessoa_id = request.form['pessoa_id']

        if not descricao or not instituicao or not data_inicio or not pessoa_id:
            flash("Todos os campos obrigatórios devem ser preenchidos!", "danger")
            return redirect(url_for('capacitacao.adicionar_capacitacao'))

        nova_capacitacao = Capacitacao(
            descricao=descricao,
            instituicao=instituicao,
            data_inicio=data_inicio,
            data_fim=data_fim if data_fim else None,
            certificado=certificado,
            pessoa_id=pessoa_id
        )

        db.session.add(nova_capacitacao)
        db.session.commit()
        flash("Capacitação adicionada com sucesso!", "success")
        return redirect(url_for('capacitacao.listar_capacitacoes'))

    return render_template('capacitacao/form.html', pessoas=pessoas)


# Rota para editar uma capacitação
@capacitacao_bp.route('/capacitacoes/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    capacitacao = Capacitacao.query.get_or_404(id)
    pessoas = Pessoa.query.all()

    if request.method == 'POST':
        capacitacao.descricao = request.form['descricao']
        capacitacao.instituicao = request.form['instituicao']
        capacitacao.data_inicio = request.form['data_inicio']
        capacitacao.data_fim = request.form.get('data_fim', None)
        capacitacao.certificado = True if 'certificado' in request.form else False
        capacitacao.pessoa_id = request.form['pessoa_id']

        db.session.commit()
        flash("Capacitação atualizada com sucesso!", "success")
        return redirect(url_for('capacitacao.listar_capacitacoes'))

    return render_template('capacitacao/form.html', capacitacao=capacitacao, pessoas=pessoas)


# Rota para deletar uma capacitação
@capacitacao_bp.route('/capacitacoes/deletar/<int:id>', methods=['POST'])
def deletar(id):
    capacitacao = Capacitacao.query.get_or_404(id)
    db.session.delete(capacitacao)
    db.session.commit()
    flash("Capacitação removida com sucesso!", "success")
    return redirect(url_for('capacitacao.listar_capacitacoes'))
