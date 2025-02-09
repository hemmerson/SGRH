from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import db
from models.models import Profissao
from routes import profissao_bp

# Rota para listar profissões
@profissao_bp.route('/profissoes')
def listar():
    profissoes = Profissao.query.all()
    return render_template('profissao/listar.html', profissoes=profissoes)

# Rota para adicionar uma nova profissão
@profissao_bp.route('/profissoes/nova', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        descricao = request.form['descricao']
        salario_base = request.form['salario_base']
        data_inicio = request.form['data_inicio']

        if not descricao or not salario_base or not data_inicio:
            flash("Todos os campos são obrigatórios!", "danger")
            return redirect(url_for('profissao.adicionar_profissao'))

        nova_profissao = Profissao(
            descricao=descricao,
            salario_base=salario_base,
            data_inicio=data_inicio
        )

        db.session.add(nova_profissao)
        db.session.commit()
        flash("Profissão adicionada com sucesso!", "success")
        return redirect(url_for('profissao.listar_profissoes'))

    return render_template('profissao/form.html')

# Rota para editar uma profissão
@profissao_bp.route('/profissoes/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    profissao = Profissao.query.get_or_404(id)

    if request.method == 'POST':
        profissao.descricao = request.form['descricao']
        profissao.salario_base = request.form['salario_base']
        profissao.data_inicio = request.form['data_inicio']

        db.session.commit()
        flash("Profissão atualizada com sucesso!", "success")
        return redirect(url_for('profissao.listar_profissoes'))

    return render_template('profissao/form.html', profissao=profissao)

# Rota para deletar uma profissão
@profissao_bp.route('/profissoes/deletar/<int:id>', methods=['POST'])
def deletar(id):
    profissao = Profissao.query.get_or_404(id)
    db.session.delete(profissao)
    db.session.commit()
    flash("Profissão removida com sucesso!", "success")
    return redirect(url_for('profissao.listar_profissoes'))
