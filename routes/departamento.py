from flask import render_template, request, redirect, url_for, flash
from app import db
from models.models import Departamento
from routes import departamento_bp
from utils import process_form_data


@departamento_bp.route('/departamentos')
def listar():
    departamentos = Departamento.query.all()
    config = {
        'title': 'Lista de Departamentos',
        'registros': departamentos,
        'novo_registro_url': url_for('departamento.cadastrar'),
        'novo_registro_texto': 'Novo Departamento',
        'editar_url': url_for('departamento.editar', id=0)[:-1] + '%s',
        'excluir_url': url_for('departamento.excluir', id=0)[:-1] + '%s',
        'mensagem_confirmacao': 'Tem certeza que deseja excluir este departamento?',
        'mensagem_lista_vazia': 'Nenhum departamento cadastrado ainda.',
        'colunas': [
            {'campo': 'nome', 'label': 'Nome do Departamento'},
            {
                'campo': 'profissoes',
                'label': 'Quantidade de Cargos',
                'formato': 'custom',
                'custom_value': lambda obj: len(obj.profissoes)
            }
        ],
        'acoes': True
    }
    return render_template('components/generic_list.html', **config)

@departamento_bp.route('/departamentos/novo', methods=['GET', 'POST'])
def cadastrar():
    config = get_departamento_form_config()

    if request.method == 'POST':
        dados = process_form_data(request.form, config['campos'])
        try:
            novo_departamento = Departamento(**dados)
            db.session.add(novo_departamento)
            db.session.commit()
            flash('Departamento cadastrado com sucesso!', 'success')
            return redirect(url_for('departamento.listar'))
        except:
            db.session.rollback()
            flash('Erro ao cadastrar departamento', 'danger')

    return render_template('components/generic_form.html', **config)

@departamento_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    departamento = Departamento.query.get_or_404(id)
    config = get_departamento_form_config(departamento)

    if request.method == 'POST':
        dados = process_form_data(request.form, config['campos'])

        try:
            for key, value in dados.items():
                setattr(departamento, key, value)
            db.session.commit()
            flash('Departamento atualizado com sucesso!', 'success')
            return redirect(url_for('departamento.listar'))
        except:
            db.session.rollback()
            flash('Erro ao editar departamento', 'danger')

    return render_template('components/generic_form.html', **config)

@departamento_bp.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    departamento = Departamento.query.get_or_404(id)
    db.session.delete(departamento)
    db.session.commit()
    flash('Departamento excluído com sucesso!', 'danger')
    return redirect(url_for('departamento.listar'))

def get_departamento_form_config(departamento=None):
    return {
        'titulo': 'Departamento',
        'registro': departamento,
        'voltar_url': url_for('departamento.listar'),
        'campos': [
            {
                'tipo': 'text',
                'nome': 'nome',
                'label': 'Nome',
                'required': True
            }
        ]
    }