from flask import render_template, request, redirect, url_for, flash
from app import db
from models.models import Departamento
from routes import departamento_bp


@departamento_bp.route('/')
def listar():
    departamentos = Departamento.query.all()
    return render_template('departamento/listar.html', departamentos=departamentos)

@departamento_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']

        departamento = Departamento(
            nome=nome
        )
        db.session.add(departamento)
        db.session.commit()
        flash('Departamento cadastrado com sucesso!', 'success')
        return redirect(url_for('departamento.listar'))

    return render_template('departamento/form.html')

@departamento_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    departamento = Departamento.query.get_or_404(id)

    if request.method == 'POST':
        departamento.nome = request.form['nome']

        db.session.commit()
        flash('Departamento atualizado com sucesso!', 'success')
        return redirect(url_for('departamento.listar'))

    return render_template('departamento/form.html', departamento=departamento)

@departamento_bp.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    departamento = Departamento.query.get_or_404(id)
    db.session.delete(departamento)
    db.session.commit()
    flash('Departamento excluído com sucesso!', 'danger')
    return redirect(url_for('departamento.listar'))
