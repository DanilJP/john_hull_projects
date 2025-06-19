import streamlit as st
import numpy as np

st.set_page_config(page_title="📉 Avaliação de Contratos a Termo", layout="centered")
st.title("📉 Avaliação de Contratos a Termo")

st.markdown("""
### 📘 Fórmula Geral
\[
f = (F_0 - K) \cdot e^{-rT}
\]

Onde:
- **f**: valor do contrato a termo hoje  
- **F₀**: preço a termo atual  
- **K**: preço de entrega (acordado no passado)  
- **r**: taxa livre de risco anual (capitalização contínua)  
- **T**: tempo restante até o vencimento (em anos)
""")

st.markdown("### 🧮 Calculadora Interativa")

col1, col2 = st.columns(2)
with col1:
    F0 = st.number_input("Preço a termo atual (F₀)", value=26.28)
    K = st.number_input("Preço de entrega acordado (K)", value=24.0)
with col2:
    r = st.number_input("Taxa livre de risco anual (%)", value=10.0) / 100
    T = st.number_input("Tempo restante até o vencimento (em anos)", value=0.5)

# Valor do contrato a termo
f = (F0 - K) * np.exp(-r * T)

st.markdown(f"""
#### 💰 Valor Atual do Contrato:
- f = **${f:.2f}**
""")

st.markdown("---")

with st.expander("📚 Exemplo Hull 5.4"):
    st.markdown("""
- S₀ = 25  
- K = 24  
- r = 10% ao ano (0,10)  
- T = 0,5 anos (6 meses)  
- F₀ = 25e^{0.10 × 0.5} = 26,28  
- f = (26,28 - 24)e^{-0.10 × 0.5} = 2,17  
    """)

st.caption("Baseado na seção 5.7 do livro 'Opções, Futuros e Outros Derivativos' de John Hull.")
