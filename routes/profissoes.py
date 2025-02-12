from flask import render_template, request, redirect, url_for, flash

from db import db
from models.models import Profissao, Departamento
from routes import profissao_bp
from utils import process_form_data

@profissao_bp.route('/profissoes')
def listar():
    profissoes = Profissao.query.all()
    config = {
        'title': 'Lista de Profissões',
        'registros': profissoes,
        'novo_registro_url': url_for('profissao.cadastrar'),
        'novo_registro_texto': 'Nova Profissão',
        'editar_url': url_for('profissao.editar', id=0)[:-1] + '%s',  # Remove o 0 e adiciona %s para formatação
        'excluir_url': url_for('profissao.excluir', id=0)[:-1] + '%s',
        'mensagem_confirmacao': 'Tem certeza que deseja excluir esta profissão?',
        'mensagem_lista_vazia': 'Nenhuma profissão cadastrada ainda.',
        'colunas': [
            {'campo': 'nome_cargo', 'label': 'Nome do cargo'},
            {'campo': 'descricao', 'label': 'Descrição'},
            {'campo': 'salario_base', 'label': 'Salário Base', 'formato': 'moeda'},
            {
                'campo': 'departamento',
                'label': 'Departamento',
                'formato': 'relacionamento',
                'campo_relacionamento': 'nome'
            }
        ],
        'acoes': True
    }
    return render_template('components/generic_list.html', **config)


@profissao_bp.route('/profissoes/nova', methods=['GET', 'POST'])
def cadastrar():
    config = get_profissao_form_config()

    if request.method == 'POST':
        dados = process_form_data(request.form, config['campos'])

        try:
            nova_profissao = Profissao(**dados)
            db.session.add(nova_profissao)
            db.session.commit()
            flash('Profissao cadastrada com sucesso!', 'success')
            return redirect(url_for('profissao.listar'))
        except ValueError:
            flash("Salário base deve ser um valor numérico válido!", "danger")
        except Exception as e:
            db.session.rollback()
            flash('Erro ao cadastrar profissao. Por favor, tente novamente.', 'danger')

    return render_template('components/generic_form.html', **config)


@profissao_bp.route('/profissoes/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    profissao = Profissao.query.get_or_404(id)
    config = get_profissao_form_config(profissao)

    if request.method == 'POST':
        dados = process_form_data(request.form, config['campos'])

        try:
            for key, value in dados.items():
                setattr(profissao, key, value)

            db.session.commit()
            flash("Profissão atualizada com sucesso!", "success")
            return redirect(url_for('profissao.listar'))
        except ValueError:
            flash("Salário base deve ser um valor numérico válido!", "danger")
        except Exception as e:
            db.session.rollback()
            flash("Erro ao atualizar profissão. Por favor, tente novamente.", "danger")

    return render_template('components/generic_form.html', **config)


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

def get_profissao_form_config(profissao=None):
    return {
        'titulo': 'Profissao',
        'registro': profissao,
        'voltar_url': url_for('profissao.listar'),
        'campos': [
            {
                'tipo': 'text',
                'nome': 'nome_cargo',
                'label': 'Cargo',
                'required': True,
            },
            {
                'tipo': 'textarea',
                'nome': 'descricao',
                'label': 'Descrição',
                'required': True,
            },
            {
                'tipo': 'number',
                'nome': 'salario_base',
                'label': 'Salário Base',
                'required': True,
            },
            {
                'tipo': 'select',
                'nome': 'departamento_id',
                'label': 'Departamento',
                'required': True,
                'opcoes': [
                    {'value': d.id, 'label': d.nome}
                    for d in Departamento.query.all()
                ]
            }
        ]
    }