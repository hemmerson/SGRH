from flask import render_template, request, redirect, url_for, flash
from app import db
from models.models import Pessoa, Profissao
from routes import bp_pessoa

@bp_pessoa.route('/')
def listar():
    pessoas = Pessoa.query.all()
    return render_template('pessoa/listar.html', pessoas=pessoas)

@bp_pessoa.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    profissoes = Profissao.query.all()

    if request.method == 'POST':
        nome = request.form['nome']
        data_nascimento = request.form['data_nascimento']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        email = request.form['email']
        profissao_id = request.form['profissao_id']

        nova_pessoa = Pessoa(
            nome=nome,
            data_nascimento=data_nascimento,
            endereco=endereco,
            telefone=telefone,
            email=email,
            profissao_id=profissao_id
        )
        db.session.add(nova_pessoa)
        db.session.commit()
        flash('Pessoa cadastrada com sucesso!', 'success')
        return redirect(url_for('pessoas.listar'))

    return render_template('pessoa/form.html', profissoes=profissoes)

@bp_pessoa.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    pessoa = Pessoa.query.get_or_404(id)
    profissoes = Profissao.query.all()

    if request.method == 'POST':
        pessoa.nome = request.form['nome']
        pessoa.data_nascimento = request.form['data_nascimento']
        pessoa.endereco = request.form['endereco']
        pessoa.telefone = request.form['telefone']
        pessoa.email = request.form['email']
        pessoa.profissao_id = request.form['profissao_id']

        db.session.commit()
        flash('Pessoa atualizada com sucesso!', 'success')
        return redirect(url_for('pessoas.listar'))

    return render_template('pessoa/form.html', pessoa=pessoa, profissoes=profissoes)

@bp_pessoa.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    pessoa = Pessoa.query.get_or_404(id)
    db.session.delete(pessoa)
    db.session.commit()
    flash('Pessoa excluída com sucesso!', 'danger')
    return redirect(url_for('pessoas.listar'))
