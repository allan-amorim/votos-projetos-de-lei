2+2
from utils import strings
from utils.formats import formatar_valor

def resumo_divida(dados):
    # Calcular as somas para Allan e Melanie
    soma_allan = sum(item[strings.vl_morzao_divida] for item in dados.values() if item[strings.nm_usuario] == 'Allan' and not item[strings.bl_quitado])
    soma_melanie = sum(item[strings.vl_morzao_divida] for item in dados.values() if item[strings.nm_usuario] == 'Melanie' and not item[strings.bl_quitado])

    # Determinar quem deve a quem e a diferença
    if soma_allan > soma_melanie:
        diferenca = soma_allan - soma_melanie
        texto = f'Melanie deve {formatar_valor(diferenca)} a Allan'
    elif soma_melanie > soma_allan:
        diferenca = soma_melanie - soma_allan
        texto = f'Allan deve {formatar_valor(diferenca)} a Melanie'
    else:
        texto = 'Allan e Melanie estão quites'

    return texto


def calcular_valor_individual(dados: dict):
    
    """
    Retorna {usuario: {mês do gasto: {subcategoria: {valor e %valor}}}}
    """
    
    d = [{**row, strings.id_gasto: _} for _, row in dados.items()]
    agregacao = {}
    for linha in d:
        for sub in strings.subcategorias:
            if linha[strings.nm_usuario] not in agregacao:
                agregacao[linha[strings.nm_usuario]] = {}
            if linha[strings.dt_gasto].strftime("%Y/%m") not in agregacao[linha[strings.nm_usuario]]:
                agregacao[linha[strings.nm_usuario]][linha[strings.dt_gasto].strftime("%Y/%m")] = {}
            if sub not in (
                agregacao[linha[strings.nm_usuario]][linha[strings.dt_gasto].strftime("%Y/%m")]
            ):
                agregacao[
                    linha[strings.nm_usuario]
                ][
                    linha[strings.dt_gasto].strftime("%Y/%m")
                ][
                    sub
                ] = {'Valor': 0}
            if (
                (linha[strings.nm_subcategoria] == sub) 
                or (not linha[strings.nm_subcategoria] and sub == 'Outros')
            ):
                agregacao[
                    linha[strings.nm_usuario]
                ][
                    linha[strings.dt_gasto].strftime("%Y/%m")
                ][
                    sub
                ][
                    'Valor'
                ] += linha['vl_gasto']

    for u in agregacao:
        for g in agregacao[u]:
            for s in agregacao[u][g]:
                total_valor = sum(agregacao[u][g][m]['Valor'] for m in agregacao[u][g])
                agregacao[u][g][s]['% Valor'] = (
                    agregacao[u][g][s]['Valor']/total_valor if total_valor != 0 else 0
                )

    return agregacao

# def calcular_valor_individual(dados: dict):
    
#     """
#     Retorna {usuario: {mês do gasto: {subcategoria: {valor e %valor}}}}
#     """
    
#     d = [{**row, strings.id_gasto: _} for _, row in dados.items()]
#     agregacao = {}
#     for linha in d:
#         for sub in strings.subcategorias:
#             if linha[strings.nm_usuario] not in agregacao:
#                 agregacao[linha[strings.nm_usuario]] = {}
#             if linha[strings.dt_gasto].strftime("%Y/%m") not in agregacao[linha[strings.nm_usuario]]:
#                 agregacao[linha[strings.nm_usuario]][linha[strings.dt_gasto].strftime("%Y/%m")] = {}
#             if sub not in (
#                 agregacao[linha[strings.nm_usuario]][linha[strings.dt_gasto].strftime("%Y/%m")]
#             ):
#                 agregacao[
#                     linha[strings.nm_usuario]
#                 ][
#                     linha[strings.dt_gasto].strftime("%Y/%m")
#                 ][
#                     sub
#                 ] = {'Valor': 0}
#             if (
#                 (linha[strings.nm_subcategoria] == sub) 
#                 or (not linha[strings.nm_subcategoria] and sub == 'Outros')
#             ):
#                 agregacao[
#                     linha[strings.nm_usuario]
#                 ][
#                     linha[strings.dt_gasto].strftime("%Y/%m")
#                 ][
#                     sub
#                 ][
#                     'Valor'
#                 ] += linha['vl_gasto']

#     for usuario in agregacao:
#         for mes in agregacao[usuario]:
#             for subc in agregacao[usuario][mes]:
#                 if 'Mês' not in agregacao[usuario][mes][subc]['Mês']:
#                     agregacao[usuario][mes][subc]['Mês'] =
#                 total_valor = sum(agregacao[usuario][mes][m]['Valor'] for m in agregacao[usuario][mes])
#                 agregacao[usuario][mes][subc]['% Valor'] = (
#                     agregacao[usuario][mes][subc]['Valor']/total_valor if total_valor != 0 else 0
#                 )

#     for usuario in agregacao:
#         for mes in agregacao:
#             for subc, v2 in agregacao[mes].items():
#                 if mes not in subcategs:
#                     subcategs[mes] = {'Mês': mes}
#                 subcategs[mes][subc] = v2['Valor']
#                 subcategs[mes][f'% {subc}'] = v2['% Valor']

#     return agregacao