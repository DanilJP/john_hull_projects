import streamlit as st

# Página principal otimizada para celular
st.set_page_config(page_title="Projetos Quant", layout="centered")

st.title("📊 Welcome to Profy")
st.markdown("Explore projetos práticos em **Finanças Quantitativas**.")

# Expanders com agrupamentos claros e compactos
with st.expander("💳 Crédito"):
    st.page_link("pages/Modelagem_Risco_Credito.py", label="👉 Modelagem de Risco de Crédito")
    st.page_link("pages/Analise_Risco_Credito.py", label="👉 Análise Exploratória")

with st.expander("💹 Derivativos"):
    st.page_link("pages/Calculadora_NDF.py", label="👉 Black-Scholes")
    st.page_link("pages/Precificacao_BlackScholes.py", label="👉 Black-Scholes")
    st.page_link("pages/Simulacao_MonteCarlo.py", label="👉 Monte Carlo")
    st.page_link("pages/Precificacao_Binomial.py", label="👉 Binomial")
    st.page_link("pages/Greeks_Opcoes.py", label="👉 Greeks")

with st.expander("📈 Gestão de Risco"):
    st.page_link("pages/Value_at_Risk.py", label="👉 VaR")
    st.page_link("pages/Stress_Testing.py", label="👉 Stress Testing")
    st.page_link("pages/PFE_Calculation.py", label="👉 PFE")

with st.expander("📊 Análise Quantitativa"):
    st.page_link("pages/Series_Temporais.py", label="👉 Séries Temporais")
    st.page_link("pages/Backtesting_Modelos.py", label="👉 Backtesting")
    st.page_link("pages/Optimizacao_Portfolio.py", label="👉 Portfólio")

st.markdown("---")
st.markdown("<center><small>Desenvolvido por Daniel Juliano | Versão Beta 🚧</small></center>", unsafe_allow_html=True)
