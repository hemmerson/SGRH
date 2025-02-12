from flask import render_template, request, redirect, url_for, flash
from db import db
from models.models import FolhaPagamento, Pessoa
from routes import folha_pagamento_bp
from utils import process_form_data

@folha_pagamento_bp.route('/folhas-pagamento')
def listar():
    folhas = FolhaPagamento.query.all()
    config = {
        'title': 'Lista de Folhas de Pagamento',
        'registros': folhas,
        'novo_registro_url': url_for('folha_pagamento.cadastrar'),
        'novo_registro_texto': 'Nova Folha de Pagamento',
        'editar_url': url_for('folha_pagamento.editar', id=0)[:-1] + '%s',
        'excluir_url': url_for('folha_pagamento.excluir', id=0)[:-1] + '%s',
        'mensagem_confirmacao': 'Tem certeza que deseja excluir esta folha de pagamento?',
        'mensagem_lista_vazia': 'Nenhuma folha de pagamento cadastrada ainda.',
        'colunas': [
            {
                'campo': 'pessoas',
                'label': 'Pessoa',
                'formato': 'lista',
                'campo_lista': 'nome'
            },
            {'campo': 'mes_referencia', 'label': 'Mês/Ano'},
            {'campo': 'data_pagamento', 'label': 'Data Pagamento', 'formato': 'data'},
            {'campo': 'salario_bruto', 'label': 'Salário Bruto', 'formato': 'moeda'},
            {'campo': 'descontos', 'label': 'Descontos', 'formato': 'moeda'},
            {'campo': 'beneficios', 'label': 'Benefícios', 'formato': 'moeda'},
            {'campo': 'salario_liquido', 'label': 'Salário Líquido', 'formato': 'moeda'}
        ],
        'acoes': True
    }
    return render_template('components/generic_list.html', **config)

@folha_pagamento_bp.route('/folhas/nova', methods=['GET', 'POST'])
def cadastrar():
    config = get_folha_pagamento_form_config()

    if request.method == 'POST':
        dados = process_form_data(request.form, config['campos'])
        try:
            # Remove pessoa_id dos dados pois não é uma coluna direta
            pessoa_id = dados.pop('pessoa_id')
            pessoa = Pessoa.query.get(pessoa_id)

            if not pessoa:
                raise ValueError("Pessoa não encontrada")

            nova_folha = FolhaPagamento(**dados)
            # Adiciona a pessoa à folha de pagamento
            nova_folha.pessoas.append(pessoa)

            db.session.add(nova_folha)
            db.session.commit()
            flash('Folha de pagamento criada com sucesso!', 'success')
            return redirect(url_for('folha_pagamento.listar'))
        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:
            db.session.rollback()
            flash('Erro ao cadastrar folha de pagamento. Por favor tente novamente.', 'danger')

    return render_template('components/generic_form.html', **config)


@folha_pagamento_bp.route('/folhas/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    folha = FolhaPagamento.query.get_or_404(id)
    config = get_folha_pagamento_form_config(folha)

    if request.method == 'POST':
        dados = process_form_data(request.form, config['campos'])
        try:
            # Remove e atualiza relacionamento com pessoa
            pessoa_id = dados.pop('pessoa_id')
            pessoa = Pessoa.query.get(pessoa_id)

            if not pessoa:
                raise ValueError("Pessoa não encontrada")

            # Limpa relacionamentos existentes e adiciona o novo
            folha.pessoas.clear()
            folha.pessoas.append(pessoa)

            # Atualiza demais campos
            for key, value in dados.items():
                setattr(folha, key, value)

            db.session.commit()
            flash("Folha de pagamento atualizada com sucesso!", "success")
            return redirect(url_for('folha_pagamento.listar'))
        except ValueError as e:
            flash(str(e), "danger")
        except Exception as e:
            db.session.rollback()
            flash("Erro ao atualizar folha de pagamento. Por favor, tente novamente.", "danger")

    return render_template('components/generic_form.html', **config)

@folha_pagamento_bp.route('/folhas/deletar/<int:id>', methods=['POST'])
def excluir(id):
    folha = FolhaPagamento.query.get_or_404(id)
    try:
        db.session.delete(folha)
        db.session.commit()
        flash("Folha de pagamento removida com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash("Erro ao remover folha de pagamento.", "danger")

    return redirect(url_for('folha_pagamento.listar'))

def get_folha_pagamento_form_config(folha=None):
    return {
        'titulo': 'Folha de Pagamento',
        'registro': folha,
        'voltar_url': url_for('folha_pagamento.listar'),
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
                'nome': 'mes_referencia',
                'label': 'Mês/Ano Referência (MM/YYYY)',
                'required': True,
                'help_text': 'Formato: MM/YYYY (ex: 02/2024)'
            },
            {
                'tipo': 'date',
                'nome': 'data_pagamento',
                'label': 'Data de Pagamento',
                'required': True
            },
            {
                'tipo': 'number',
                'nome': 'salario_bruto',
                'label': 'Salário Bruto',
                'required': True,
                'step': '0.01',
                'min': '0'
            },
            {
                'tipo': 'number',
                'nome': 'descontos',
                'label': 'Descontos',
                'required': True,
                'step': '0.01',
                'min': '0',
                'valor_padrao': '0.00'
            },
            {
                'tipo': 'number',
                'nome': 'beneficios',
                'label': 'Benefícios',
                'required': True,
                'step': '0.01',
                'min': '0',
                'valor_padrao': '0.00'
            },
            {
                'tipo': 'number',
                'nome': 'salario_liquido',
                'label': 'Salário Líquido',
                'required': True,
                'step': '0.01',
                'min': '0'
            }
        ]
    }