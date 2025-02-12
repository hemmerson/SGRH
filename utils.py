from datetime import datetime


def process_form_data(request_form, campos_config):
    """Processa dados do formulário baseado na configuração dos campos"""
    dados = {}

    for campo in campos_config:
        nome = campo['nome']
        tipo = campo['tipo']

        if tipo == 'checkbox':
            dados[nome] = nome in request_form
        elif tipo == 'date' and request_form.get(nome):
            dados[nome] = datetime.strptime(request_form[nome], '%Y-%m-%d').date()
        elif tipo == 'number':
            dados[nome] = float(request_form[nome]) if request_form.get(nome) else None
        else:
            dados[nome] = request_form.get(nome)

    return dados