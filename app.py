import streamlit as st
from calculations import (
    pre_embarque, pos_embarque_desconto_lc, pos_embarque_emprestimo_simples,
    factoring_exportacao, garantia, comparador_cenarios
)
from decision_assistant import gerar_decisao

st.set_page_config(page_title="Simulador Trade Finance", layout="wide")

st.title("Simulador de Operações de Trade Finance")

# Sidebar para navegação
menu = st.sidebar.selectbox("Escolha a seção", ["Simulador Individual", "Comparador de Cenários"])

if menu == "Simulador Individual":
    st.header("Simulador Individual de Produtos")

    produto = st.selectbox("Selecione o produto", [
        "Pré-embarque (Empacotamento de Crédito)",
        "Pós-embarque - Desconto de LC",
        "Pós-embarque - Empréstimo Simples",
        "Factoring de Exportação",
        "Garantia"
    ])

    # Mapeamento
    produto_key = {
        "Pré-embarque (Empacotamento de Crédito)": "pre_embarque",
        "Pós-embarque - Desconto de LC": "pos_desconto_lc",
        "Pós-embarque - Empréstimo Simples": "pos_emprestimo",
        "Factoring de Exportação": "factoring",
        "Garantia": "garantia"
    }[produto]

    # Inputs comuns para decisão
    st.subheader("Parâmetros Adicionais para Assistente de Decisão")
    col1, col2 = st.columns(2)
    with col1:
        tipo_base = st.selectbox("Tipo de Base", ["LC Confirmado", "LC Não Confirmado", "Contrato Simples", "Garantia Bancária", "Com Recurso", "Sem Recurso"])
        risco_cliente = st.selectbox("Risco do Cliente", ["Baixa", "Média", "Alta"])
    with col2:
        pais_cliente = st.text_input("País do Cliente", "Angola")
        pais_contraparte = st.text_input("País da Contraparte", "Portugal")
        sinal_preco_desvio = st.checkbox("Sinal de Preço Fora do Normal (Desvio Elevado)")

    extras = {
        'tipo_base': tipo_base,
        'risco_cliente': risco_cliente.lower(),
        'pais_cliente': pais_cliente,
        'pais_contraparte': pais_contraparte,
        'sinal_preco_desvio': sinal_preco_desvio
    }

    # Inputs específicos
    params = {}
    if produto_key == "pre_embarque":
        st.subheader("Parâmetros para Pré-Embarque")
        col1, col2 = st.columns(2)
        with col1:
            valor_lc = st.number_input("Valor da LC/Contrato (USD)", min_value=0.0, value=300000.0, step=1000.0)
            percent_financiada = st.slider("Percentagem Financiada (%)", 0.0, 100.0, 70.0) / 100
            prazo_dias = st.number_input("Prazo em Dias", min_value=1, value=60)
        with col2:
            taxa_anual = st.number_input("Taxa de Juro Anual (%)", min_value=0.0, value=12.0, step=0.1)
            comissao_percent = st.number_input("Comissão (%)", min_value=0.0, value=0.5, step=0.1)
        params = {
            'valor_lc': valor_lc,
            'percent_financiada': percent_financiada,
            'prazo_dias': prazo_dias,
            'taxa_anual': taxa_anual,
            'comissao_percent': comissao_percent
        }
        resultados = pre_embarque(**params)

    elif produto_key == "pos_desconto_lc":
        st.subheader("Parâmetros para Pós-Embarque - Desconto de LC")
        col1, col2 = st.columns(2)
        with col1:
            valor_lc = st.number_input("Valor da LC (USD)", min_value=0.0, value=300000.0, step=1000.0)
            prazo_dias = st.number_input("Prazo até Vencimento (Dias)", min_value=1, value=90)
        with col2:
            taxa_desconto_anual = st.number_input("Taxa de Desconto Anual (%)", min_value=0.0, value=8.0, step=0.1)
            comissao_percent = st.number_input("Comissão (%)", min_value=0.0, value=0.2, step=0.1)
        params = {
            'valor_lc': valor_lc,
            'prazo_dias': prazo_dias,
            'taxa_desconto_anual': taxa_desconto_anual,
            'comissao_percent': comissao_percent
        }
        resultados = pos_embarque_desconto_lc(**params)

    elif produto_key == "pos_emprestimo":
        st.subheader("Parâmetros para Pós-Embarque - Empréstimo Simples")
        col1, col2 = st.columns(2)
        with col1:
            valor_emprestimo = st.number_input("Valor do Empréstimo (USD)", min_value=0.0, value=300000.0, step=1000.0)
            prazo_dias = st.number_input("Prazo (Dias)", min_value=1, value=90)
        with col2:
            taxa_anual = st.number_input("Taxa de Juro Anual (%)", min_value=0.0, value=10.0, step=0.1)
            comissao_percent = st.number_input("Comissão (%)", min_value=0.0, value=0.5, step=0.1)
        params = {
            'valor_emprestimo': valor_emprestimo,
            'prazo_dias': prazo_dias,
            'taxa_anual': taxa_anual,
            'comissao_percent': comissao_percent
        }
        resultados = pos_embarque_emprestimo_simples(**params)

    elif produto_key == "factoring":
        st.subheader("Parâmetros para Factoring de Exportação")
        col1, col2 = st.columns(2)
        with col1:
            valor_faturas = st.number_input("Valor Nominal das Faturas (USD)", min_value=0.0, value=300000.0, step=1000.0)
            percent_adiantamento = st.slider("Percentagem de Adiantamento (%)", 0.0, 100.0, 80.0) / 100
            prazo_dias = st.number_input("Prazo Médio (Dias)", min_value=1, value=60)
        with col2:
            taxa_anual = st.number_input("Taxa de Juro Anual (%)", min_value=0.0, value=10.0, step=0.1)
            comissao_percent = st.number_input("Comissão de Serviço (%)", min_value=0.0, value=1.0, step=0.1)
        params = {
            'valor_faturas': valor_faturas,
            'percent_adiantamento': percent_adiantamento,
            'prazo_dias': prazo_dias,
            'taxa_anual': taxa_anual,
            'comissao_percent': comissao_percent
        }
        resultados = factoring_exportacao(**params)

    elif produto_key == "garantia":
        st.subheader("Parâmetros para Garantia")
        col1, col2 = st.columns(2)
        with col1:
            valor_garantia = st.number_input("Valor da Garantia (USD)", min_value=0.0, value=1000000.0, step=1000.0)
            prazo_meses = st.number_input("Prazo em Meses", min_value=1, value=18)
        with col2:
            comissao_anual_percent = st.number_input("Comissão Anual (%)", min_value=0.0, value=2.5, step=0.1)
            taxa_fixa_emissao = st.number_input("Taxa Fixa de Emissão (USD)", min_value=0.0, value=500.0, step=10.0)
            percent_deposito = st.slider("Percentagem de Depósito Colateral (%)", 0.0, 100.0, 20.0)
        params = {
            'valor_garantia': valor_garantia,
            'prazo_meses': prazo_meses,
            'comissao_anual_percent': comissao_anual_percent,
            'taxa_fixa_emissao': taxa_fixa_emissao,
            'percent_deposito': percent_deposito
        }
        resultados = garantia(**params)

    # Exibir resultados
    st.subheader("Resultados Numéricos")
    for key, value in resultados.items():
        if isinstance(value, float):
            st.write(f"{key.replace('_', ' ').title()}: {value:,.2f}")
        else:
            st.write(f"{key.replace('_', ' ').title()}: {value:,.0f}")

    # Assistente de Decisão
    st.subheader("Assistente de Decisão")
    decisao_texto = gerar_decisao(produto_key, params, extras)
    st.markdown(decisao_texto)

elif menu == "Comparador de Cenários":
    st.header("Comparador de Cenários")

    st.subheader("Parâmetros Globais")
    col1, col2 = st.columns(2)
    with col1:
        valor_base = st.number_input("Valor Base da Operação (USD)", min_value=0.0, value=300000.0, step=1000.0)
        prazo_dias = st.number_input("Prazo em Dias", min_value=1, value=90)
    with col2:
        # Parâmetros por produto
        st.subheader("Desconto de LC")
        desconto_lc_taxa = st.number_input("Taxa Desconto (%)", min_value=0.0, value=8.0, step=0.1, key="lc_taxa")
        desconto_lc_comissao = st.number_input("Comissão (%)", min_value=0.0, value=0.2, step=0.1, key="lc_com")

        st.subheader("Empréstimo Pós-Embarque")
        emprestimo_taxa = st.number_input("Taxa (%)", min_value=0.0, value=10.0, step=0.1, key="emp_taxa")
        emprestimo_comissao = st.number_input("Comissão (%)", min_value=0.0, value=0.5, step=0.1, key="emp_com")

        st.subheader("Factoring")
        factoring_adiantamento = st.slider("Adiantamento (%)", 0.0, 100.0, 80.0) / 100
        factoring_taxa = st.number_input("Taxa (%)", min_value=0.0, value=10.0, step=0.1, key="fac_taxa")
        factoring_comissao = st.number_input("Comissão (%)", min_value=0.0, value=1.0, step=0.1, key="fac_com")

    if st.button("Comparar"):
        custos, mais_barato = comparador_cenarios(
            valor_base, prazo_dias,
            desconto_lc_taxa, desconto_lc_comissao,
            emprestimo_taxa, emprestimo_comissao,
            factoring_adiantamento, factoring_taxa, factoring_comissao
        )

        st.subheader("Resultados da Comparação")
        for produto, vals in custos.items():
            st.write(f"**{produto.replace('_', ' ').title()}**: Custo Absoluto: {vals['custo_absoluto']:,.2f} USD, Efetivo: {vals['custo_efetivo']:.2f}%")

        st.success(f"O produto mais barato é: {mais_barato.replace('_', ' ').title()}")