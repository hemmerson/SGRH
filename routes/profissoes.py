from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from app import db
from models.models import Profissao, Pessoa
from routes import profissoes_bp

@profissoes_bp.route('/profissoes')
def listar():
    profissoes = Profissao.query.all()
    return render_template('profissao/listar.html', profissoes=profissoes)

@profissoes_bp.route('/profissoes/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    pessoas = Pessoa.query.all()
    if request.method == 'POST':
        try:
            profissao = Profissao(
                descricao=request.form['descricao'],
                salario_base=float(request.form['salario_base']),
                data_inicio=datetime.strptime(request.form['data_inicio'], '%Y-%m-%d'),
                pessoa_id=int(request.form['pessoa_id'])
            )
            db.session.add(profissao)
            db.session.commit()
            flash('Profissão cadastrada com sucesso!', 'success')
            return redirect(url_for('profissoes.listar'))
        except Exception as e:
            flash('Erro ao cadastrar profissão.', 'danger')
            db.session.rollback()

    return render_template('profissao/form.html', pessoas=pessoas)

@profissoes_bp.route('/profissoes/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    pessoas = Pessoa.query.all()

    profissao = Profissao.query.get_or_404(id)


    if request.method == 'POST':
        try:
            profissao.descricao = request.form['descricao']
            profissao.salario_base = float(request.form['salario_base'])
            profissao.data_inicio = datetime.strptime(request.form['data_inicio'], '%Y-%m-%d')
            profissao.pessoa_id = int(request.form['pessoa_id'])

            db.session.commit()
            flash('Profissão atualizada com sucesso!', 'success')
            return redirect(url_for('profissoes.listar'))
        except Exception as e:
            flash('Erro ao atualizar profissão.', 'danger')
            db.session.rollback()

    return render_template('profissao/form.html', profissao=profissao, pessoas=pessoas)

@profissoes_bp.route('/profissoes/excluir/<int:id>', methods=['POST'])
def excluir(id):
    profissao = Profissao.query.get_or_404(id)
    try:
        db.session.delete(profissao)
        db.session.commit()
        flash('Profissão excluída com sucesso!', 'success')
    except Exception as e:
        flash('Erro ao excluir profissão.', 'danger')
        db.session.rollback()

    return redirect(url_for('profissoes.listar'))