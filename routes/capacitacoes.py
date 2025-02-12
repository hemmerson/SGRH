from flask import render_template, request, redirect, url_for, flash

from db import db
from models.models import Capacitacao, Pessoa
from routes import capacitacao_bp
from utils import process_form_data


@capacitacao_bp.route('/capacitacoes')
def listar():
    capacitacoes = Capacitacao.query.all()
    config = {
        'title': 'Lista de Capacitações',
        'registros': capacitacoes,
        'novo_registro_url': url_for('capacitacao.cadastrar'),
        'novo_registro_texto': 'Nova Capacitação',
        'editar_url': url_for('capacitacao.editar', id=0)[:-1] + '%s',
        'excluir_url': url_for('capacitacao.excluir', id=0)[:-1] + '%s',
        'mensagem_confirmacao': 'Tem certeza que deseja excluir esta capacitação?',
        'mensagem_lista_vazia': 'Nenhuma capacitação cadastrada ainda.',
        'colunas': [
            {'campo': 'titulo', 'label': 'Titulo'},
            {'campo': 'instituicao', 'label': 'Instituição'},
            {'campo': 'data_inicio', 'label': 'Data Início', 'formato': 'data'},
            {'campo': 'data_fim', 'label': 'Data Fim', 'formato': 'data'},
            {
                'campo': 'certificado',
                'label': 'Certificado',
                'formato': 'booleano',
                'valores_booleanos': ['Sim', 'Não']
            },
            {
                'campo': 'pessoa',
                'label': 'Pessoa',
                'formato': 'relacionamento',
                'campo_relacionamento': 'nome'
            }
        ],
        'acoes': True
    }
    return render_template('components/generic_list.html', **config)


@capacitacao_bp.route('/capacitacoes/nova', methods=['GET', 'POST'])
def cadastrar():
    config = get_capacitacao_form_config()

    if request.method == 'POST':
        dados = process_form_data(request.form, config['campos'])
        try:
            nova_capacitacao = Capacitacao(**dados)
            db.session.add(nova_capacitacao)
            db.session.commit()
            flash('Capacitacao criada com sucesso!', 'success')
            return redirect(url_for('capacitacao.listar'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao cadastrar capacitação. Por favor tente novamente.', 'danger')

    return render_template('components/generic_form.html', **config)


@capacitacao_bp.route('/capacitacoes/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    capacitacao = Capacitacao.query.get_or_404(id)
    config = get_capacitacao_form_config(capacitacao)

    if request.method == 'POST':
        dados = process_form_data(request.form, config['campos'])

        try:
            for key, value in dados.items():
                setattr(capacitacao, key, value)

            db.session.commit()
            flash("Capacitação atualizada com sucesso!", "success")
            return redirect(url_for('capacitacao.listar'))
        except ValueError as e:
            flash(str(e), "danger")
        except Exception as e:
            db.session.rollback()
            flash("Erro ao atualizar capacitação. Por favor, tente novamente.", "danger")

    return render_template('components/generic_form.html', **config)


@capacitacao_bp.route('/capacitacoes/deletar/<int:id>', methods=['POST'])
def excluir(id):
    capacitacao = Capacitacao.query.get_or_404(id)
    try:
        db.session.delete(capacitacao)
        db.session.commit()
        flash("Capacitação removida com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash("Erro ao remover capacitação.", "danger")

    return redirect(url_for('capacitacao.listar'))

def get_capacitacao_form_config(capacitacao=None):
    return {
        'titulo': 'Capacitação',
        'registro': capacitacao,
        'voltar_url': url_for('capacitacao.listar'),
        'campos': [
            {
                'tipo': 'select',
                'nome': 'pessoa_id',
                'label': 'Pessoa',
                'required': True,
                'opcoes': [
                    {'value': p.id, 'label': p.nome}
                    for p in Pessoa.query.all()
                ]
            },
            {
                'tipo': 'text',
                'nome': 'titulo',
                'label': 'Título',
                'required': True
            },
            {
                'tipo': 'textarea',
                'nome': 'descricao',
                'label': 'Descrição',
                'required': True,
                'rows': 3
            },
            {
                'tipo': 'text',
                'nome': 'instituicao',
                'label': 'Instituição de Ensino',
                'required': True
            },
            {
                'tipo': 'date',
                'nome': 'data_inicio',
                'label': 'Data de Início',
                'required': True
            },
            {
                'tipo': 'date',
                'nome': 'data_fim',
                'label': 'Data de Conclusão'
            },
            {
                'tipo': 'checkbox',
                'nome': 'certificado',
                'label': 'Certificado?',
                'valor_padrao': True
            }
        ]
    }