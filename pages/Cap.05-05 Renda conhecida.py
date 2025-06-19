import streamlit as st
import numpy as np

st.set_page_config(page_title="💸 Preço a Termo com Renda Conhecida", layout="centered")
st.title("💸 Preço a Termo com Renda Conhecida (Hull 5.2)")

st.markdown("""
### 📘 Fórmula
Quando o ativo oferece rendas futuras **previsíveis**, a fórmula do preço a termo se ajusta:

\[
F_0 = (S_0 - I) \cdot e^{rT}
\]

Onde:
- **F₀**: preço a termo
- **S₀**: preço à vista do ativo
- **I**: valor presente da renda futura (ex: dividendos ou cupons)
- **r**: taxa livre de risco (capitalização contínua)
- **T**: tempo até o vencimento
""")

st.markdown("### 🧮 Calculadora Interativa")

col1, col2 = st.columns(2)
with col1:
    S0 = st.number_input("Preço à vista do ativo (S₀)", value=900.0)
    r = st.number_input("Taxa livre de risco anual (%)", value=4.0) / 100
    T = st.number_input("Tempo até o vencimento (T - em anos)", value=9/12)

with col2:
    renda_bruta = st.text_input("Rendas previstas separadas por vírgula (ex: 40)", value="40")
    tempos_renda = st.text_input("Meses até cada renda (ex: 4)", value="4")

# Cálculo do valor presente das rendas
# try:
r_ano = 1
rendas = [float(r.strip()) for r in renda_bruta.split(',')]
tempos = [float(t.strip())/12 for t in tempos_renda.split(',')]
if len(rendas) != len(tempos):
    st.error("❌ O número de rendas e tempos deve ser igual.")
else:
    I = sum([r * np.exp(-r_ano * t) for r, t in zip(rendas, tempos)])
    F0 = (S0 - I) * np.exp(r * T)

    st.markdown(f"""
    #### 💰 Resultado:
    - Valor presente das rendas (**I**) = ${I:.2f}  
    - Preço a termo (**F₀**) = ${F0:.2f}
    """)
# except:
#     st.warning("⏳ Aguardando entradas numéricas válidas...")

st.markdown("---")

with st.expander("📚 Exemplo Hull"):
    st.markdown("""
- S₀ = 900  
- Cupom de $40 após 4 meses  
- Taxas: 3% (4 meses) e 4% (9 meses)  
- I = 40 · e^(-0,03·4/12) ≈ 39,60  
- F₀ = (900 - 39,60) · e^(0,04·9/12) ≈ 886,60  
    """)

st.caption("Baseado na seção 5.5 do livro 'Opções, Futuros e Outros Derivativos' de John Hull.")
