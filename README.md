# Trade Finance Simulator

Este projeto é um simulador interativo em Python usando Streamlit para operações de Trade Finance, simulando o trabalho de um analista/gestor em um banco. Inclui duas partes principais:

1. **Simulador Numérico**: Calcula custos para produtos como pré-embarque, pós-embarque, desconto de LC, factoring e garantias.
2. **Assistente de Decisão**: Gera texto explicativo baseado em práticas de Trade Finance e AML/TBML, sugerindo aprovações ou mitigações.

## Funcionalidades

- Simulação individual de produtos com inputs específicos e outputs de custos.
- Comparador de cenários para o mesmo valor e prazo.
- Assistente de decisão com análise de riscos e recomendações.

## Requisitos

- Python 3.8+
- Streamlit

Instale as dependências com:
```
pip install -r requirements.txt
```

## Como Executar

Execute o aplicativo com:
```
streamlit run app.py
```

## Estrutura do Projeto

- `app.py`: Aplicativo principal Streamlit.
- `calculations.py`: Funções de cálculo para cada produto.
- `decision_assistant.py`: Lógica para gerar textos explicativos de decisão.
- `requirements.txt`: Dependências Python.