import streamlit as st
import numpy as np

st.set_page_config(page_title="📈 Preço a Termo - Hull Eq. 5.1", layout="centered")
st.title("📈 Preço a Termo - Ativo sem Renda")

st.markdown("""
### 📘 Fórmula
A fórmula de precificação para um ativo de investimento que **não oferece renda**:

\[
F_0 = S_0 \cdot e^{rT}
\]

Onde:
- **F₀**: preço a termo do contrato
- **S₀**: preço à vista do ativo
- **r**: taxa livre de risco (capitalização contínua)
- **T**: tempo até vencimento (em anos)
""")

st.markdown("### 🧮 Calculadora Interativa")

col1, col2 = st.columns(2)
with col1:
    S0 = st.number_input("Preço à vista do ativo (S₀)", min_value=0.0, value=930.0)
    r = st.number_input("Taxa livre de risco anual (r) (%)", min_value=0.0, value=6.0) / 100

with col2:
    T = st.number_input("Tempo até o vencimento (T - em anos)", min_value=0.0, value=4/12)

# Cálculo
F0 = S0 * np.exp(r * T)

st.markdown(f"""
#### 💰 Resultado:
**Preço a termo (F₀)** = ${F0:.2f}
""")

st.markdown("---")

with st.expander("📚 Exemplos do Hull"):
    st.markdown("""
- Exemplo: Um título com cupom zero custa **$930** hoje.
- A taxa de juros de 4 meses é **6% ao ano**.
- Usando a fórmula:  
  \[
  F_0 = 930 \t e^{0.06 \cdot \frac{4}{12}} \approx 948,79
  \]
""")

st.caption("Baseado no capítulo 5.4 do livro 'Opções, Futuros e Outros Derivativos' de John Hull.")
