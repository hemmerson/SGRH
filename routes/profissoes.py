from flask import render_template, request, redirect, url_for, flash
from decimal import Decimal
from db import db
from models.models import Profissao, Departamento
from routes import profissao_bp


@profissao_bp.route('/profissoes')
def listar():
    profissoes = Profissao.query.all()
    return render_template('profissao/listar.html', profissoes=profissoes)


@profissao_bp.route('/profissoes/nova', methods=['GET', 'POST'])
def cadastrar():
    departamentos = Departamento.query.all()

    if request.method == 'POST':
        nome_cargo = request.form['nome_cargo']
        descricao = request.form['descricao']
        salario_base = request.form['salario_base']
        departamento_id = request.form['departamento_id']

        if not descricao or not salario_base or not nome_cargo or not departamento_id:
            flash("Todos os campos são obrigatórios!", "danger")
            return redirect(url_for('profissao.cadastrar'))

        try:
            salario_base = Decimal(salario_base.replace(',', '.'))
        except:
            flash("Salário base deve ser um valor numérico válido!", "danger")
            return redirect(url_for('profissao.cadastrar'))

        nova_profissao = Profissao(
            descricao=descricao,
            salario_base=salario_base,
            nome_cargo=nome_cargo,
            departamento_id=departamento_id
        )

        try:
            db.session.add(nova_profissao)
            db.session.commit()
            flash("Profissão adicionada com sucesso!", "success")
            return redirect(url_for('profissao.listar'))
        except Exception as e:
            db.session.rollback()
            flash("Erro ao adicionar profissão. Por favor, tente novamente.", "danger")
            return redirect(url_for('profissao.cadastrar'))

    return render_template('profissao/form.html', departamentos=departamentos)


@profissao_bp.route('/profissoes/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    profissao = Profissao.query.get_or_404(id)
    departamentos = Departamento.query.all()

    if request.method == 'POST':
        try:
            profissao.nome_cargo = request.form['nome_cargo']
            profissao.descricao = request.form['descricao']
            profissao.salario_base = Decimal(request.form['salario_base'].replace(',', '.'))
            profissao.departamento_id = request.form['departamento_id']

            db.session.commit()
            flash("Profissão atualizada com sucesso!", "success")
            return redirect(url_for('profissao.listar'))
        except ValueError:
            flash("Salário base deve ser um valor numérico válido!", "danger")
        except Exception as e:
            db.session.rollback()
            flash("Erro ao atualizar profissão. Por favor, tente novamente.", "danger")

    return render_template('profissao/form.html', profissao=profissao, departamentos=departamentos)


@profissao_bp.route('/profissoes/deletar/<int:id>', methods=['POST'])
def excluir(id):
    profissao = Profissao.query.get_or_404(id)
    try:
        db.session.delete(profissao)
        db.session.commit()
        flash("Profissão removida com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash("Erro ao remover profissão. Verifique se não há pessoas vinculadas.", "danger")

    return redirect(url_for('profissao.listar'))