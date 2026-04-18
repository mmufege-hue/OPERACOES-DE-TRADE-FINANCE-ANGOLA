"""
Módulo do Assistente de Decisão.
Gera texto explicativo baseado em práticas de Trade Finance e AML/TBML.
"""

# Configurações ajustáveis: limites considerados "normais"
LIMITE_PRAZO_PRE_EMBARQUE = (30, 90)  # dias
LIMITE_PERCENT_FINANCIADA = (0.6, 0.85)
LIMITE_CUSTO_EFETIVO_ALTO = 5.0  # % no período
LIMITE_PRAZO_GARANTIA = (6, 24)  # meses

# Mapa de risco por país (exemplo simples; ajustar conforme necessário)
RISCO_PAIS = {
    'Angola': 'normal',
    'Portugal': 'baixo',
    'Estados Unidos': 'baixo',
    'Irã': 'alto',
    'Coreia do Norte': 'alto',
    # Adicionar mais conforme necessário
}

def avaliar_risco_pais(pais):
    """Retorna nível de risco do país."""
    return RISCO_PAIS.get(pais, 'normal')

def gerar_decisao_pre_embarque(params, extras):
    """
    Gera texto para pré-embarque.
    :param params: Dict com parâmetros numéricos
    :param extras: Dict com extras (tipo_base, risco_cliente, pais_cliente, pais_contraparte, sinal_preco_desvio)
    :return: Texto explicativo
    """
    valor_lc = params.get('valor_lc', 0)
    percent = params.get('percent_financiada', 0)
    prazo = params.get('prazo_dias', 0)
    taxa = params.get('taxa_anual', 0)
    comissao = params.get('comissao_percent', 0)
    custo_efetivo = params.get('custo_efetivo_percent', 0)

    tipo_base = extras.get('tipo_base', 'contrato simples')
    risco_cliente = extras.get('risco_cliente', 'média')
    pais_cliente = extras.get('pais_cliente', 'Angola')
    pais_contraparte = extras.get('pais_contraparte', 'Angola')
    sinal_preco = extras.get('sinal_preco_desvio', False)

    texto = f"""
**Resumo do Cenário:** Operação de pré-embarque de {valor_lc:,.0f} USD, financiando {percent*100:.0f}% por {prazo} dias a {taxa:.1f}% aa, com comissão de {comissao:.1f}%, resultando em custo efetivo de {custo_efetivo:.2f}% no período.

**Análise Técnica/Comercial:** O prazo de {prazo} dias {'está dentro do típico' if LIMITE_PRAZO_PRE_EMBARQUE[0] <= prazo <= LIMITE_PRAZO_PRE_EMBARQUE[1] else 'pode ser considerado longo/curto'}. A percentagem financiada de {percent*100:.0f}% {'é razoável' if LIMITE_PERCENT_FINANCIADA[0] <= percent <= LIMITE_PERCENT_FINANCIADA[1] else 'está fora do normal'}. O custo efetivo {'está aceitável' if custo_efetivo <= LIMITE_CUSTO_EFETIVO_ALTO else 'é elevado e pode exigir reflexão'}.

**Análise Prudencial/Risco:** Baseado em {tipo_base}, o risco é {'baixo' if 'confirmado' in tipo_base.lower() else 'médio'}. Risco do cliente é {risco_cliente}. Risco país cliente: {avaliar_risco_pais(pais_cliente)}, contraparte: {avaliar_risco_pais(pais_contraparte)}. O banco avalia risco de crédito e país; LCs são regidas por regras internacionais que priorizam documentos conformes.

**Sugestão de Decisão e Mitigantes:** {'Aprovar, sujeito a políticas internas de crédito e AML.' if (LIMITE_PRAZO_PRE_EMBARQUE[0] <= prazo <= LIMITE_PRAZO_PRE_EMBARQUE[1] and LIMITE_PERCENT_FINANCIADA[0] <= percent <= LIMITE_PERCENT_FINANCIADA[1] and custo_efetivo <= LIMITE_CUSTO_EFETIVO_ALTO and risco_cliente in ['baixa', 'média'] and avaliar_risco_pais(pais_contraparte) != 'alto') else 'Aprovar com mitigantes (ex.: colateral adicional, garantias).' if sinal_preco or risco_cliente == 'alta' or avaliar_risco_pais(pais_contraparte) == 'alto' else 'Rever/Recusar devido a parâmetros extremos.'} {'Recomenda-se reforço de due diligence devido a possível desvio de preço.' if sinal_preco else ''}
    """
    return texto.strip()

def gerar_decisao_pos_desconto_lc(params, extras):
    """
    Gera texto para pós-embarque desconto LC.
    """
    valor_lc = params.get('valor_lc', 0)
    prazo = params.get('prazo_dias', 0)
    taxa = params.get('taxa_desconto_anual', 0)
    comissao = params.get('comissao_percent', 0)
    custo_efetivo = params.get('custo_efetivo_percent', 0)

    tipo_base = extras.get('tipo_base', 'LC não confirmado')
    risco_cliente = extras.get('risco_cliente', 'média')
    pais_cliente = extras.get('pais_cliente', 'Angola')
    pais_contraparte = extras.get('pais_contraparte', 'Angola')
    sinal_preco = extras.get('sinal_preco_desvio', False)

    texto = f"""
**Resumo do Cenário:** Desconto de LC de {valor_lc:,.0f} USD, prazo {prazo} dias, taxa {taxa:.1f}% aa, comissão {comissao:.1f}%, custo efetivo {custo_efetivo:.2f}% no período.

**Análise Técnica/Comercial:** O desconto de LC é eficiente para liquidez imediata. Custo efetivo {'aceitável' if custo_efetivo <= LIMITE_CUSTO_EFETIVO_ALTO else 'elevado'}.

**Análise Prudencial/Risco:** Baseia-se em LC irrevogável ({'confirmada' if 'confirmado' in tipo_base.lower() else 'não confirmada'}), regida por UCP 600. Risco residual: documentos discrepantes e risco país/banco emissor. Risco cliente: {risco_cliente}, país cliente: {avaliar_risco_pais(pais_cliente)}, contraparte: {avaliar_risco_pais(pais_contraparte)}.

**Sugestão de Decisão e Mitigantes:** {'Aprovar.' if custo_efetivo <= LIMITE_CUSTO_EFETIVO_ALTO and 'confirmado' in tipo_base.lower() and risco_cliente != 'alta' else 'Aprovar com mitigantes (garantias adicionais).' if sinal_preco or avaliar_risco_pais(pais_contraparte) == 'alto' else 'Rever/Recusar.'} {'Verificações AML adicionais devido a desvio de preço.' if sinal_preco else ''}
    """
    return texto.strip()

def gerar_decisao_pos_emprestimo(params, extras):
    """
    Gera texto para pós-embarque empréstimo simples.
    """
    valor = params.get('valor_emprestimo', 0)
    prazo = params.get('prazo_dias', 0)
    taxa = params.get('taxa_anual', 0)
    comissao = params.get('comissao_percent', 0)
    custo_efetivo = params.get('custo_efetivo_percent', 0)

    tipo_base = extras.get('tipo_base', 'contrato simples')
    risco_cliente = extras.get('risco_cliente', 'média')
    pais_cliente = extras.get('pais_cliente', 'Angola')
    pais_contraparte = extras.get('pais_contraparte', 'Angola')
    sinal_preco = extras.get('sinal_preco_desvio', False)

    texto = f"""
**Resumo do Cenário:** Empréstimo pós-embarque de {valor:,.0f} USD, prazo {prazo} dias, taxa {taxa:.1f}% aa, comissão {comissao:.1f}%, custo efetivo {custo_efetivo:.2f}% no período.

**Análise Técnica/Comercial:** Adequado para financiar recebíveis. Custo efetivo {'razoável' if custo_efetivo <= LIMITE_CUSTO_EFETIVO_ALTO else 'alto'}.

**Análise Prudencial/Risco:** Risco de crédito do cliente e contraparte. Tipo base: {tipo_base}. Risco cliente: {risco_cliente}, países: cliente {avaliar_risco_pais(pais_cliente)}, contraparte {avaliar_risco_pais(pais_contraparte)}.

**Sugestão de Decisão e Mitigantes:** {'Aprovar.' if custo_efetivo <= LIMITE_CUSTO_EFETIVO_ALTO and risco_cliente != 'alta' else 'Aprovar com mitigantes.' if sinal_preco else 'Rever.'} {'Reforçar EDD por possível TBML.' if sinal_preco else ''}
    """
    return texto.strip()

def gerar_decisao_factoring(params, extras):
    """
    Gera texto para factoring.
    """
    valor = params.get('valor_faturas', 0)
    adiantamento = params.get('percent_adiantamento', 0)
    prazo = params.get('prazo_dias', 0)
    taxa = params.get('taxa_anual', 0)
    comissao = params.get('comissao_percent', 0)
    custo_efetivo = params.get('custo_efetivo_percent', 0)

    tipo_base = extras.get('tipo_base', 'sem recurso')  # Assumir sem recurso se não especificado
    risco_cliente = extras.get('risco_cliente', 'média')
    pais_cliente = extras.get('pais_cliente', 'Angola')
    pais_contraparte = extras.get('pais_contraparte', 'Angola')
    sinal_preco = extras.get('sinal_preco_desvio', False)

    texto = f"""
**Resumo do Cenário:** Factoring de {valor:,.0f} USD, adiantamento {adiantamento*100:.0f}%, prazo {prazo} dias, taxa {taxa:.1f}% aa, comissão {comissao:.1f}%, custo efetivo {custo_efetivo:.2f}% no período.

**Análise Técnica/Comercial:** Fornece liquidez imediata e gestão de crédito. Adiantamento {'típico' if 0.7 <= adiantamento <= 0.9 else 'baixo/alto'}.

**Análise Prudencial/Risco:** {'Com recurso: banco assume risco de crédito. Sem recurso: risco permanece com exportador.' if 'recurso' in tipo_base.lower() else 'Risco de crédito do comprador.'} Risco cliente: {risco_cliente}, países: {avaliar_risco_pais(pais_cliente)}, {avaliar_risco_pais(pais_contraparte)}.

**Sugestão de Decisão e Mitigantes:** {'Aprovar.' if custo_efetivo <= LIMITE_CUSTO_EFETIVO_ALTO and risco_cliente != 'alta' else 'Aprovar com mitigantes.' if sinal_preco else 'Rever.'} {'Due diligence adicional.' if sinal_preco else ''}
    """
    return texto.strip()

def gerar_decisao_garantia(params, extras):
    """
    Gera texto para garantia.
    """
    valor = params.get('valor_garantia', 0)
    prazo = params.get('prazo_meses', 0)
    comissao = params.get('comissao_anual_percent', 0)
    taxa_fixa = params.get('taxa_fixa_emissao', 0)
    deposito = params.get('percent_deposito', 0)

    tipo_base = extras.get('tipo_base', 'garantia bancária')
    risco_cliente = extras.get('risco_cliente', 'média')
    pais_cliente = extras.get('pais_cliente', 'Angola')
    pais_contraparte = extras.get('pais_contraparte', 'Angola')
    sinal_preco = extras.get('sinal_preco_desvio', False)

    texto = f"""
**Resumo do Cenário:** Garantia de {valor:,.0f} USD, prazo {prazo} meses, comissão {comissao:.1f}% aa, taxa fixa {taxa_fixa:,.0f}, depósito {deposito:.0f}%.

**Análise Técnica/Comercial:** Prazo {'razoável' if LIMITE_PRAZO_GARANTIA[0] <= prazo <= LIMITE_PRAZO_GARANTIA[1] else 'extremo'}. Depósito colateral adequado para mitigar risco.

**Análise Prudencial/Risco:** Banco assume risco de desempenho/crédito do cliente, baseado em URDG 758. Tipo: {tipo_base}. Risco cliente: {risco_cliente}, países: {avaliar_risco_pais(pais_cliente)}, {avaliar_risco_pais(pais_contraparte)}.

**Sugestão de Decisão e Mitigantes:** {'Aprovar.' if LIMITE_PRAZO_GARANTIA[0] <= prazo <= LIMITE_PRAZO_GARANTIA[1] and risco_cliente != 'alta' else 'Aprovar com mitigantes.' if sinal_preco else 'Rever.'} {'Verificações AML.' if sinal_preco else ''}
    """
    return texto.strip()

# Função geral para chamar a certa
def gerar_decisao(produto, params, extras):
    """
    Chama a função de decisão apropriada.
    :param produto: Nome do produto
    :param params: Parâmetros numéricos
    :param extras: Parâmetros extras
    :return: Texto
    """
    if produto == 'pre_embarque':
        return gerar_decisao_pre_embarque(params, extras)
    elif produto == 'pos_desconto_lc':
        return gerar_decisao_pos_desconto_lc(params, extras)
    elif produto == 'pos_emprestimo':
        return gerar_decisao_pos_emprestimo(params, extras)
    elif produto == 'factoring':
        return gerar_decisao_factoring(params, extras)
    elif produto == 'garantia':
        return gerar_decisao_garantia(params, extras)
    else:
        return "Produto não reconhecido."