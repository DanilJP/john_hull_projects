import streamlit as st

# Página principal otimizada para celular
st.set_page_config(page_title="Projetos Quant", layout="centered")

st.title("📊 Bem vindo John Hull Projects")
st.markdown("Explore projetos práticos em **Finanças Quantitativas**.")

with st.expander("💳 Capítulo 4 - Taxas de Juros"):
    st.page_link("pages/Cap.04-01 Tipos de taxa.py", label="👉 4.1 Tipos de taxa")
    st.page_link("pages/Cap.04-02 Medição de taxas de juros.py", label="👉 4.1 Medição de taxas de juros")
    st.page_link("pages/Cap.04-03 Taxas zero.py", label="👉 4.3 Taxas zero")
    st.page_link("pages/Cap.04-04 Apreçamento de títulos.py", label="👉 4.4 Apreçamento de títulos")
    st.page_link("pages/Cap.04-05 Determinação das taxas zero do tesouro.py", label="👉 4.5 Determinação das taxas zero do tesouro")
    st.page_link("pages/Cap.04-06 Taxas forward.py", label="👉 4.6 Taxas forward")
    st.page_link("pages/Cap.04-07 Contratos de taxa forward.py", label="👉 4.7 Contrato de taxa forward")
    st.page_link("pages/Cap.04-08 Duração.py", label="👉 4.8 Duração")
    st.page_link("pages/Cap.04-09 Convexidade.py", label="👉 4.9 Convexidade")
    st.page_link("pages/Cap.04-10 Teorias da Estrutura a Termo das Taxas de Juros.py", label="👉 4.10 Teorias da Estrutura a Termo das Taxas de Juros")

with st.expander("💳 Capítulo 5 - Determinação de preços a termo e futuros"):
    st.page_link("pages/Cap.05-01 Ativos de investimento versus ativos de consumo.py", label="👉 5.1 Ativos de investimento versus ativos de consumo")
    st.page_link("pages/Cap.05-02 Venda a descoberto.py", label="👉 5.2 Venda a descoberto")
    st.page_link("pages/Cap.05-03 Premissas e notação.py", label="👉 5.3 Premissas e notação")
    st.page_link("pages/Cap.05-04 Preço a termo de um ativo de investimento.py", label="👉 5.4 Preço a termo de um ativo de investimento")
    st.page_link("pages/Cap.05-05 Renda conhecida.py", label="👉 5.5 Renda conhecida")
    st.page_link("pages/Cap.05-06 Rendimento conhecido.py", label="👉 5.6 Rendimento conhecido")
    st.page_link("pages/Cap.05-07 Avaliação de contratos a termo.py", label="👉 5.7 Avaliação de contratos a termo")
    st.page_link("pages/Cap.05-08 Os preços a termos e os preços futuros são iguais.py", label="👉 5.8 Os preços a termos e os preços futuros são iguais?")


with st.expander("💳 Capítulo 24 - Risco de Crédito"):
    st.page_link("pages/Cap.24-02 Probabilidades de inadimplência históricas.py", label="👉 24.2 Probabilidades de inadimplência históricas")
    st.page_link("pages/Cap.24-04 Estimativa de probabilidade de inadimplência a partir de spreads de rendimentos de títulos.py", label="👉 24.4 Estimativa de probabilidade de inadimplência a partir de spreads de rendimentos de títulos")
    st.page_link("pages/Cap.24-06 - Utilizando preços de ações para estimar probabilidades de inadimplência.py", label="👉 24.6 Utilizando preços de ações para estimar probabilidades de inadimplência")

st.markdown("---")
st.markdown("<center><small>Desenvolvido por Daniel Juliano | Versão Beta 🚧</small></center>", unsafe_allow_html=True)
