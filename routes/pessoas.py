from flask import render_template, request, redirect, url_for, flash
from app import db
from models.models import Pessoa, Profissao
from routes import bp_pessoa
from utils import process_form_data


@bp_pessoa.route('/pessoas')
def listar():
    pessoas = Pessoa.query.all()
    config = {
        'title': 'Lista de Pessoas',
        'registros': pessoas,
        'novo_registro_url': url_for('pessoas.cadastrar'),
        'novo_registro_texto': 'Nova Pessoa',
        'editar_url': url_for('pessoas.editar', id=0)[:-1] + '%s',
        'excluir_url': url_for('pessoas.excluir', id=0)[:-1] + '%s',
        'mensagem_confirmacao': 'Tem certeza que deseja excluir esta pessoa?',
        'mensagem_lista_vazia': 'Nenhuma pessoa cadastrada ainda.',
        'colunas': [
            {'campo': 'nome', 'label': 'Nome'},
            {'campo': 'data_nascimento', 'label': 'Data de Nascimento', 'formato': 'data'},
            {'campo': 'telefone', 'label': 'Telefone'},
            {'campo': 'email', 'label': 'E-mail'},
            {'campo': 'data_admissao', 'label': 'Data de Admissão', 'formato': 'data'},
            {
                'campo': 'profissao',
                'label': 'Cargo',
                'formato': 'relacionamento',
                'campo_relacionamento': 'nome_cargo'
            }
        ],
        'acoes': True
    }
    return render_template('components/generic_list.html', **config)

@bp_pessoa.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    config = get_pessoa_form_config()

    if request.method == 'POST':
        dados = process_form_data(request.form, config['campos'])

        try:
            nova_pessoa = Pessoa(**dados)
            db.session.add(nova_pessoa)
            db.session.commit()
            flash('Pessoa cadastrada com sucesso!', 'success')
            return redirect(url_for('pessoas.listar'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao cadastrar a Pessoa. Por favor tente novamente', 'danger')

    return render_template('components/generic_form.html', **config)

@bp_pessoa.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    pessoa = Pessoa.query.get_or_404(id)
    config = get_pessoa_form_config(pessoa)

    if request.method == 'POST':
        dados = process_form_data(request.form, config['campos'])

        try:
            for key, value in dados.items():
                setattr(pessoa, key, value)

            db.session.commit()
            flash('Pessoa atualizada com sucesso!', 'success')
            return redirect(url_for('pessoas.listar'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao editar a Pessoa. Por favor tente novamente.', 'danger')

    return render_template('components/generic_form.html', **config)

@bp_pessoa.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    pessoa = Pessoa.query.get_or_404(id)
    db.session.delete(pessoa)
    db.session.commit()
    flash('Pessoa excluída com sucesso!', 'danger')
    return redirect(url_for('pessoas.listar'))


def get_pessoa_form_config(pessoa=None):
    return {
        'titulo': 'Pessoa',
        'registro': pessoa,
        'voltar_url': url_for('pessoas.listar'),
        'campos': [
            {
                'tipo': 'text',
                'nome': 'nome',
                'label': 'Nome Completo',
                'required': True
            },
            {
                'tipo': 'date',
                'nome': 'data_nascimento',
                'label': 'Data de Nascimento',
                'required': True
            },
            {
                'tipo': 'textarea',
                'nome': 'endereco',
                'label': 'Endereço',
                'required': True
            },
            {
                'tipo': 'text',
                'nome': 'telefone',
                'label': 'Telefone',
                'required': True,
                'help_text': 'Digite apenas números'
            },
            {
                'tipo': 'email',
                'nome': 'email',
                'label': 'E-mail',
                'required': True
            },
            {
                'tipo': 'date',
                'nome': 'data_admissao',
                'label': 'Data de Admissão',
                'required': True
            },
            {
                'tipo': 'select',
                'nome': 'profissao_id',
                'label': 'Cargo',
                'required': True,
                'opcoes': [
                    {'value': p.id, 'label': p.nome_cargo}
                    for p in Profissao.query.all()
                ]
            }
        ]
    }