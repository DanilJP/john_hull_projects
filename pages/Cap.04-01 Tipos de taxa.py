import streamlit as st
import pandas as pd
import numpy as np

# Configuração visual
st.set_page_config(page_title="Projetos Quant")
st.markdown("<h1 style='text-align: left;'>💼 Tipos de taxa</h1>", unsafe_allow_html=True)

st.markdown("As **taxas de juros** representam o custo do dinheiro. Elas variam conforme o **risco de crédito**: quanto maior o risco de inadimplência, maior a taxa exigida.\
             Normalmente, são expressas em **pontos-base** (1 ponto-base = 0,01% ao ano).")

st.divider()

with st.expander("🟢 Taxas do Tesouro"):
    st.markdown("""
    - Emitidas por governos em sua **própria moeda**.
    - Consideradas **livres de risco**.
    - Exemplos:
        - Letras e títulos do Tesouro dos EUA (dólar)
        - Títulos do governo japonês (iene)
    - Assume-se que o governo **não dá calote** em sua própria moeda.
    """)

with st.expander("🔵 LIBOR (London Interbank Offered Rate)"):
    st.markdown("""
    - Taxa interbancária de **curto prazo sem garantia**.
    - Baseada em estimativas de bancos com rating **AA**.
    - Usada globalmente como **referência em derivativos**, como swaps.
    - Publicada diariamente pela **British Bankers Association (BBA)**.
    - Críticas por **possível manipulação** e uso de cotações não baseadas em transações reais.
    - Está sendo gradualmente **substituída por taxas baseadas em mercado**.
    """)

with st.expander("🟣 Taxa de Juros Básica (Fed Funds)"):
    st.markdown("""
    - Taxa **overnight** entre bancos nos EUA via **Federal Reserve**.
    - Média ponderada das taxas de empréstimos realizados no dia.
    - Monitorada e influenciada pelo **banco central americano**.
    - Equivalentes internacionais:
        - 🇬🇧 SONIA (Reino Unido)
        - 🇪🇺 EONIA (Zona do Euro)
    """)

with st.expander("🟠 Taxa Repo"):
    st.markdown("""
    - Empréstimos **garantidos com títulos**.
    - A instituição vende um título com acordo de **recomprá-lo por um valor maior**.
    - Muito baixo risco de crédito, pois há **colateral**.
    - Repos mais comuns:
        - **Repo overnight**
        - **Term repos** (prazo mais longo)
    - Costuma ter taxa **menor que empréstimos não garantidos**.
    """)

with st.expander("⚪ Taxa Livre de Risco"):
    st.markdown("""
    - Base para **avaliação de derivativos**.
    - Tradicionalmente, a **LIBOR** era usada, mas não é 100% livre de risco.
    - Hoje, são consideradas alternativas **mais seguras** baseadas em mercado.
    - O tema é aprofundado no **Capítulo 9** do livro.
    """)

st.info("Este conteúdo é um resumo baseado no livro **'Opções, Futuros e Outros Derivativos'**, de John Hull.")
