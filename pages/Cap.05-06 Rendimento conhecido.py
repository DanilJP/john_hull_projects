import streamlit as st
import numpy as np

st.set_page_config(page_title="📈 Preço a Termo com Rendimento Conhecido", layout="centered")
st.title("📈 Preço a Termo com Rendimento Conhecido")

st.markdown("""
### 📘 Fórmula
Quando o ativo fornece **rendimento proporcional ao seu preço** (como um dividend yield contínuo):

\[
F_0 = S_0 \cdot e^{(r - q)T}
\]

Onde:
- **F₀**: preço a termo
- **S₀**: preço à vista do ativo
- **r**: taxa livre de risco (capitalização contínua)
- **q**: taxa de rendimento contínuo do ativo
- **T**: tempo até vencimento
""")

st.markdown("### 🧮 Calculadora Interativa")

col1, col2 = st.columns(2)
with col1:
    S0 = st.number_input("Preço à vista do ativo (S₀)", value=25.0)
    r = st.number_input("Taxa livre de risco anual (%)", value=10.0) / 100
    T = st.number_input("Tempo até o vencimento (T - em anos)", value=0.5)

with col2:
    q = st.number_input("Taxa de rendimento anual do ativo (%)", value=3.96) / 100

# Cálculo do preço a termo
F0 = S0 * np.exp((r - q) * T)

st.markdown(f"""
#### 💰 Resultado:
- Preço a termo (**F₀**) = ${F0:.2f}
""")

st.markdown("---")

with st.expander("📚 Exemplo Hull 5.3"):
    st.markdown("""
- S₀ = 25  
- r = 10% ao ano (0,10)  
- q = 3,96% ao ano (0,0396)  
- T = 6 meses = 0,5 anos  

\[
F_0 = 25 \cdot e^{(0.10 - 0.0396) \cdot 0.5} = 25.00
\]
    """)

st.caption("Baseado na seção 5.6 do livro 'Opções, Futuros e Outros Derivativos' de John Hull.")
