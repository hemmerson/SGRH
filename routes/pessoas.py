from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from app import db
from models.models import Pessoa
from routes import pessoas_bp


@pessoas_bp.route('/pessoas')
def listar():
    pessoas = Pessoa.query.all()
    return render_template('pessoa/listar.html', pessoas=pessoas)


@pessoas_bp.route('/pessoas/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        try:
            pessoa = Pessoa(
                nome=request.form['nome'],
                data_nascimento=datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d'),
                endereco=request.form['endereco'],
                telefone=request.form['telefone'],
                email=request.form['email']
            )
            db.session.add(pessoa)
            db.session.commit()
            flash('Pessoa cadastrada com sucesso!', 'success')
            return redirect(url_for('pessoas.listar'))
        except Exception as e:
            flash('Erro ao cadastrar pessoa.', 'danger')
            db.session.rollback()

    return render_template('pessoa/form.html')


@pessoas_bp.route('/pessoas/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    pessoa = Pessoa.query.get_or_404(id)

    if request.method == 'POST':
        try:
            pessoa.nome = request.form['nome']
            pessoa.data_nascimento = datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d')
            pessoa.endereco = request.form['endereco']
            pessoa.telefone = request.form['telefone']
            pessoa.email = request.form['email']

            db.session.commit()
            flash('Pessoa atualizada com sucesso!', 'success')
            return redirect(url_for('pessoas.listar'))
        except Exception as e:
            flash('Erro ao atualizar pessoa.', 'danger')
            db.session.rollback()

    return render_template('pessoa/form.html', pessoa=pessoa)


@pessoas_bp.route('/pessoas/excluir/<int:id>', methods=['POST'])
def excluir(id):
    pessoa = Pessoa.query.get_or_404(id)
    try:
        db.session.delete(pessoa)
        db.session.commit()
        flash('Pessoa excluída com sucesso!', 'success')
    except Exception as e:
        flash('Erro ao excluir pessoa.', 'danger')
        db.session.rollback()

    return redirect(url_for('pessoas.listar'))