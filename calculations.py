"""
Módulo de cálculos para o simulador de Trade Finance.
Contém funções para calcular custos de cada produto usando juros simples (base 360 dias).
"""

def calcular_juros_simples(principal, taxa_anual, prazo_dias):
    """
    Calcula juros simples.
    :param principal: Montante principal
    :param taxa_anual: Taxa anual em %
    :param prazo_dias: Prazo em dias
    :return: Valor dos juros
    """
    return principal * (taxa_anual / 100) * (prazo_dias / 360)

def pre_embarque(valor_lc, percent_financiada, prazo_dias, taxa_anual, comissao_percent):
    """
    Simulação de pré-embarque (empacotamento de crédito).
    :param valor_lc: Valor da LC/contrato
    :param percent_financiada: Percentagem financiada (ex.: 0.7)
    :param prazo_dias: Prazo em dias
    :param taxa_anual: Taxa de juro anual em %
    :param comissao_percent: Comissão em % sobre montante financiado
    :return: Dict com resultados
    """
    montante_financiado = valor_lc * percent_financiada
    juros = calcular_juros_simples(montante_financiado, taxa_anual, prazo_dias)
    comissao = montante_financiado * (comissao_percent / 100)
    custo_total = juros + comissao
    custo_efetivo = (custo_total / montante_financiado) * 100 if montante_financiado > 0 else 0
    return {
        'montante_financiado': montante_financiado,
        'juros': juros,
        'comissao': comissao,
        'custo_total': custo_total,
        'custo_efetivo_percent': custo_efetivo
    }

def pos_embarque_desconto_lc(valor_lc, prazo_dias, taxa_desconto_anual, comissao_percent):
    """
    Pós-embarque - desconto de LC.
    :param valor_lc: Valor da LC
    :param prazo_dias: Prazo até vencimento em dias
    :param taxa_desconto_anual: Taxa de desconto anual em %
    :param comissao_percent: Comissão em % sobre valor LC
    :return: Dict com resultados
    """
    juros_desconto = calcular_juros_simples(valor_lc, taxa_desconto_anual, prazo_dias)
    comissao = valor_lc * (comissao_percent / 100)
    custo_total = juros_desconto + comissao
    valor_disponivel = valor_lc - custo_total
    custo_efetivo = (custo_total / valor_lc) * 100 if valor_lc > 0 else 0
    return {
        'juros_desconto': juros_desconto,
        'comissao': comissao,
        'custo_total': custo_total,
        'valor_disponivel_hoje': valor_disponivel,
        'custo_efetivo_percent': custo_efetivo
    }

def pos_embarque_emprestimo_simples(valor_emprestimo, prazo_dias, taxa_anual, comissao_percent):
    """
    Pós-embarque - empréstimo simples sobre recebíveis.
    :param valor_emprestimo: Valor do empréstimo
    :param prazo_dias: Prazo em dias
    :param taxa_anual: Taxa de juro anual em %
    :param comissao_percent: Comissão em % sobre empréstimo
    :return: Dict com resultados
    """
    juros = calcular_juros_simples(valor_emprestimo, taxa_anual, prazo_dias)
    comissao = valor_emprestimo * (comissao_percent / 100)
    custo_total = juros + comissao
    custo_efetivo = (custo_total / valor_emprestimo) * 100 if valor_emprestimo > 0 else 0
    return {
        'montante_financiado': valor_emprestimo,
        'juros': juros,
        'comissao': comissao,
        'custo_total': custo_total,
        'custo_efetivo_percent': custo_efetivo
    }

def factoring_exportacao(valor_faturas, percent_adiantamento, prazo_dias, taxa_anual, comissao_percent):
    """
    Factoring de Exportação.
    :param valor_faturas: Valor nominal das faturas
    :param percent_adiantamento: Percentagem de adiantamento (ex.: 0.8)
    :param prazo_dias: Prazo médio em dias
    :param taxa_anual: Taxa de juro anual sobre adiantamento em %
    :param comissao_percent: Comissão de serviço em % sobre valor nominal
    :return: Dict com resultados
    """
    adiantamento = valor_faturas * percent_adiantamento
    juros = calcular_juros_simples(adiantamento, taxa_anual, prazo_dias)
    comissao = valor_faturas * (comissao_percent / 100)
    custo_total = juros + comissao
    # Total efetivo recebido: adiantamento + (valor_faturas - adiantamento - custo_total)
    saldo_final = valor_faturas - adiantamento - custo_total
    total_efetivo = adiantamento + saldo_final
    custo_efetivo = (custo_total / valor_faturas) * 100 if valor_faturas > 0 else 0
    return {
        'adiantamento_inicial': adiantamento,
        'juros': juros,
        'comissao_servico': comissao,
        'custo_total': custo_total,
        'total_efetivo_recebido': total_efetivo,
        'custo_efetivo_percent': custo_efetivo
    }

def garantia(valor_garantia, prazo_meses, comissao_anual_percent, taxa_fixa_emissao, percent_deposito):
    """
    Garantia.
    :param valor_garantia: Valor da garantia
    :param prazo_meses: Prazo em meses
    :param comissao_anual_percent: Comissão anual em %
    :param taxa_fixa_emissao: Taxa fixa de emissão
    :param percent_deposito: Percentagem de depósito colateral
    :return: Dict com resultados
    """
    comissao_total = valor_garantia * (comissao_anual_percent / 100) * (prazo_meses / 12)
    custo_total = comissao_total + taxa_fixa_emissao
    valor_colateral = valor_garantia * (percent_deposito / 100)
    return {
        'comissao_total': comissao_total,
        'custo_total': custo_total,
        'valor_colateral_bloqueado': valor_colateral
    }

# Funções para comparador
def comparador_cenarios(valor_base, prazo_dias, desconto_lc_taxa, desconto_lc_comissao,
                        emprestimo_taxa, emprestimo_comissao,
                        factoring_adiantamento, factoring_taxa, factoring_comissao):
    """
    Compara desconto LC, empréstimo pós-embarque e factoring para mesmo valor e prazo.
    :param valor_base: Valor base da operação
    :param prazo_dias: Prazo em dias
    :param desconto_lc_taxa: Taxa desconto LC %
    :param desconto_lc_comissao: Comissão desconto LC %
    :param emprestimo_taxa: Taxa empréstimo %
    :param emprestimo_comissao: Comissão empréstimo %
    :param factoring_adiantamento: % adiantamento factoring
    :param factoring_taxa: Taxa factoring %
    :param factoring_comissao: Comissão factoring %
    :return: Dict com custos para cada
    """
    # Desconto LC
    res_lc = pos_embarque_desconto_lc(valor_base, prazo_dias, desconto_lc_taxa, desconto_lc_comissao)
    custo_lc = res_lc['custo_total']
    efetivo_lc = res_lc['custo_efetivo_percent']

    # Empréstimo pós-embarque (assumindo valor_emprestimo = valor_base)
    res_emp = pos_embarque_emprestimo_simples(valor_base, prazo_dias, emprestimo_taxa, emprestimo_comissao)
    custo_emp = res_emp['custo_total']
    efetivo_emp = res_emp['custo_efetivo_percent']

    # Factoring
    res_fac = factoring_exportacao(valor_base, factoring_adiantamento, prazo_dias, factoring_taxa, factoring_comissao)
    custo_fac = res_fac['custo_total']
    efetivo_fac = res_fac['custo_efetivo_percent']

    custos = {
        'desconto_lc': {'custo_absoluto': custo_lc, 'custo_efetivo': efetivo_lc},
        'emprestimo_pos': {'custo_absoluto': custo_emp, 'custo_efetivo': efetivo_emp},
        'factoring': {'custo_absoluto': custo_fac, 'custo_efetivo': efetivo_fac}
    }

    # Produto mais barato (menor custo absoluto)
    mais_barato = min(custos, key=lambda x: custos[x]['custo_absoluto'])

    return custos, mais_barato