import streamlit as st

# Página principal otimizada para celular
st.set_page_config(page_title="Projetos Quant", layout="centered")

st.title("📊 Bem vindo John Hull Projects")
st.markdown("Explore projetos práticos em **Finanças Quantitativas**.")


# Expanders com agrupamentos claros e compactos
with st.expander("💳 Capítulo 24 - Risco de Crédito"):
    st.page_link("pages/Cap.24-2 Probabilidades de inadimplência históricas.py", label="👉 24.2 Probabilidades de inadimplência históricas")
    st.page_link("pages/Cap.24-4 Estimativa de probabilidade de inadimplência a partir de spreads de rendimentos de títulos.py", label="👉 24.4 Estimativa de probabilidade de inadimplência a partir de spreads de rendimentos de títulos")

st.markdown("---")
st.markdown("<center><small>Desenvolvido por Daniel Juliano | Versão Beta 🚧</small></center>", unsafe_allow_html=True)
