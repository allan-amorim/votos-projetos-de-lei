from datetime import datetime
from utils import strings

def formatar_valor(texto, tipo='string'):
    """
    Formata um valor monetário ou converte entre string e número.

    Exemplo:
    >>> formatar_valor("R$ 1.234,56", tipo='string')
    'R$ 1.234,56'
    >>> formatar_valor("R$ 1.234,56", tipo='number')
    1234.56
    >>> formatar_valor("", tipo='string')
    ''
    """
    if texto == None or texto == "":
        return texto
    if tipo == 'string':
        texto = str(texto).replace("R$", "").replace(",", ".").strip()
        try:
            valor = float(texto)
            return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except ValueError:
            return "R$ 0,00"
    elif tipo == 'number':
        return float(texto.replace("R$ ", "").replace(".", "").replace(",", ".").strip())
    
def formatar_data(data, tipo='data'):
    """
    Formata uma data entre string e objeto datetime.

    Exemplo:
    >>> formatar_data("25/12/2023", tipo='data')
    datetime.datetime(2023, 12, 25, 0, 0)
    >>> formatar_data(datetime(2023, 12, 25), tipo='string')
    '25/12/2023'
    >>> formatar_data("", tipo='data')
    ''
    """
    if data == None or data == "":
        return data
    if tipo == 'data':
        return datetime.strptime(data, "%d/%m/%Y")
    elif tipo == 'string':
        return data.strftime("%d/%m/%Y")
    
def formatar_boolean(dado, tipo='string'):
    """
    Converte um valor booleano entre string ('Sim'/'Não') e boolean (True/False).

    Exemplo:
    >>> formatar_boolean(True, tipo='string')
    'Sim'
    >>> formatar_boolean('Sim', tipo='boolean')
    True
    >>> formatar_boolean('Não', tipo='boolean')
    False
    """
    if tipo == 'string':
        if dado:
            return 'Sim'
        else:
            return 'Não'
    elif tipo == 'boolean':
        if dado == 'Sim':
            return True
        elif dado == 'Não':
            return False

def formatar_dados_firebase(dados, tipo='lista'):
    """
    Formata dados do Firebase em uma lista ou dicionário, incluindo ou removendo IDs.

    Exemplo:
    >>> dados = {'123': {'nome': 'João', 'idade': 30}, '456': {'nome': 'Maria', 'idade': 25}}
    >>> formatar_dados_firebase(dados, tipo='lista')
    [{'nome': 'João', 'idade': 30, 'id': '123'}, {'nome': 'Maria', 'idade': 25, 'id': '456'}]
    >>> formatar_dados_firebase(dados, tipo='dict')
    {'123': {'nome': 'João', 'idade': 30}, '456': {'nome': 'Maria', 'idade': 25}}
    """
    if tipo == 'lista':
        return [{**row, strings.id_gasto: _} for _, row in dados.items()]
    elif tipo == 'dict':
        return {
            {id: {k: v for k, v in item.items() if k != strings.id_gasto} for id, item in dados.items()}
        }


def filtrar_dicionario(dicionario: dict, not_in: list = [], yes_in: list = []):
    """
    Filtra um dicionário com base em listas de chaves a serem incluídas ou excluídas.

    Exemplo:
    >>> dicionario = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    >>> filtrar_dicionario(dicionario, not_in=['a'], yes_in=['b', 'c'])
    {'b': 2, 'c': 3}
    >>> filtrar_dicionario(dicionario, not_in=['a'], yes_in=[])
    {'b': 2, 'c': 3, 'd': 4}
    """
    dicionario = {
        k: v for k, v in dicionario.items()
        if (k in yes_in) or (k not in not_in and not yes_in)
    }
    return dicionario

def ordenar_dicionario(dicionario: dict, campo: str, reverse: bool = True):
    """
    Ordena um dicionário com base em um campo específico de seus valores.

    Exemplo:
    >>> dicionario = {'a': {'valor': 3}, 'b': {'valor': 1}, 'c': {'valor': 2}}
    >>> ordenar_dicionario(dicionario, campo='valor', reverse=True)
    {'a': {'valor': 3}, 'c': {'valor': 2}, 'b': {'valor': 1}}
    """
    dicionario_ordenado = (
        dict(
            sorted(
                dicionario.items(), key=lambda item: item[1][campo], 
                reverse=reverse
            )
        )
    )
    return dicionario_ordenado

def juntar_dicionarios(dict_1: dict, dict_2: dict):
    """
    Combina dois dicionários em um único dicionário. Em caso de chaves repetidas, o valor do segundo dicionário prevalece.

    Exemplo:
    >>> dict_1 = {'a': 1, 'b': 2}
    >>> dict_2 = {'b': 3, 'c': 4}
    >>> juntar_dicionarios(dict_1, dict_2)
    {'a': 1, 'b': 3, 'c': 4}
    """
    dicionario = {**dict_1, **dict_2}
    return dicionario

def filtrar_dicionario_por_valor(dicionario: dict, filtro: dict = {}) -> dict:

    for key, value in filtro.items():

        dicionario = {
            k: v for k, v in dicionario.items()
            if v[key] == value
        }

    return dicionario

def somar_dicionario(dicionario: dict, campo: str) -> float:
    """
    Soma os valores de um campo específico em um dicionário.

    Exemplo:
    >>> dicionario = {'a': {'valor': 3}, 'b': {'valor': 1}, 'c': {'valor': 2}}
    >>> somar_dicionario(dicionario, campo='valor')
    6.0
    """
    soma = sum([float(item[campo]) for item in dicionario.values()])
    return soma

def agrupar_dicionario(dicionario: dict, campo: str, agg: str) -> dict:
    """
    Agrupa um dicionário com base em um campo específico de seus valores.

    Exemplo:
    >>> dicionario = {'a': {'valor': 3}, 'b': {'valor': 1}, 'c': {'valor': 2}}
    >>> agrupar_dicionario(dicionario, campo='valor')
    {3.0: ['a'], 1.0: ['b'], 2.0: ['c']}
    """
    dicionario_agrupado = {}
    for item in dicionario.values():
        chave = formatar_data(item[campo], 'string')[3:]
        if chave not in dicionario_agrupado:
            dicionario_agrupado[chave] = 0
        dicionario_agrupado[chave] += item[agg]
    return dicionario_agrupado