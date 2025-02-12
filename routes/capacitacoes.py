from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from db import db
from models.models import Capacitacao, Pessoa
from routes import capacitacao_bp


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
            {'campo': 'descricao', 'label': 'Descrição'},
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
    config = {
        'titulo': 'Capacitação',
        'registro': None,  # ou capacitacao no caso de edição
        'voltar_url': url_for('capacitacao.listar'),
        'campos': [
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
    return render_template('components/generic_form.html', **config)


@capacitacao_bp.route('/capacitacoes/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    capacitacao = Capacitacao.query.get_or_404(id)
    pessoas = Pessoa.query.all()

    if request.method == 'POST':
        try:
            capacitacao.descricao = request.form['descricao']
            capacitacao.instituicao = request.form['instituicao']
            capacitacao.data_inicio = datetime.strptime(request.form['data_inicio'], '%Y-%m-%d').date()

            data_fim = request.form.get('data_fim')
            capacitacao.data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date() if data_fim else None

            capacitacao.certificado = 'certificado' in request.form
            capacitacao.pessoa_id = request.form['pessoa_id']

            db.session.commit()
            flash("Capacitação atualizada com sucesso!", "success")
            return redirect(url_for('capacitacao.listar'))
        except ValueError as e:
            flash(str(e), "danger")
        except Exception as e:
            db.session.rollback()
            flash("Erro ao atualizar capacitação. Por favor, tente novamente.", "danger")

    return render_template('capacitacao/form.html', capacitacao=capacitacao, pessoas=pessoas)


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