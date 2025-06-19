import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="📈 Ativos de investimento versus ativos de consumo")

st.title("📊 Ativos de investimento versus ativos de consumo")

st.markdown("""
No universo de derivativos, é essencial distinguir dois tipos de ativos:

### ✅ Ativos de Investimento
- Mantidos com fins de investimento, mesmo que tenham outros usos.
- Exemplos: Ações, Títulos, Ouro, Prata.
- **É possível determinar o preço a termo/futuro via arbitragem.**

### 🚫 Ativos de Consumo
- Usados principalmente para consumo direto.
- Exemplos: Petróleo, Milho, Cobre.
- **A precificação não pode ser feita apenas com arbitragem, pois há valor no uso imediato do ativo (valor de conveniência).**

---
""")

st.header("🧮 Calculadora de Preço a Termo (ativos de investimento)")

col1, col2 = st.columns(2)

with col1:
    S = st.number_input("📈 Preço à vista (S)", value=100.0)
    r = st.number_input("🏦 Taxa de juros livre de risco (%)", value=5.0) / 100
    T = st.number_input("⏳ Tempo até vencimento (anos)", value=1.0)

with col2:
    considera_div = st.checkbox("Ativo paga dividendos?")
    if considera_div:
        q = st.number_input("📉 Taxa de dividendos (%)", value=2.0) / 100
    else:
        q = 0.0

# Cálculo do preço a termo
F = S * np.exp((r - q) * T)

st.success(f"📌 Preço a termo estimado: **R$ {F:.2f}**")

st.markdown("---")

st.caption("Cálculo baseado na fórmula de arbitragem para ativos de investimento.")
