import streamlit as st
import numpy as np

st.set_page_config(page_title="Calculadora de Juros")

# Título principal
st.markdown("<h1 style='text-align: left;'>💰 Capitalização de Juros</h1>", unsafe_allow_html=True)

# Resumo teórico
st.markdown("""
A forma como a taxa de juros é **capitalizada** (anualmente, semestralmente, mensalmente etc.) influencia diretamente o montante final de um investimento.

---

### 📌 Fórmulas importantes:

- **Capitalização com frequência m (vezes ao ano):**  
  Valor futuro = `A * (1 + R/m)^(m*n)`

- **Capitalização contínua:**  
  Valor futuro = `A * e^(R * n)`

---

### 🎯 Conversão entre taxas:

- De taxa com capitalização m para contínua:  
  `Rc = m * ln(1 + Rm/m)`

- De taxa contínua para capitalização m:  
  `Rm = m * (e^(Rc/m) - 1)`
""")

st.divider()

# Simulador de capitalização
st.markdown("### 🧮 Simule o valor futuro com capitalização composta")

A = st.number_input("💵 Valor inicial (A):", value=100.0)
R_percent = st.number_input("📈 Taxa de juros anual (%):", value=10.0, step=0.1)
n = st.number_input("📆 Tempo (anos):", value=1.0, step=0.1)
m = st.selectbox("🔁 Frequência de capitalização por ano (m):", [1, 2, 4, 12, 52, 365, 'Contínua'])

R = R_percent / 100

if m != 'Contínua':
    valor_futuro = A * (1 + R / m) ** (m * n)
else:
    valor_futuro = A * np.exp(R * n)

st.success(f"💸 Valor futuro: R$ {valor_futuro:.2f}")

st.divider()

# Conversores de taxa
st.markdown("### 🔄 Conversor de Taxas de Juros")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**➡️ De taxa com capitalização m para contínua**")
    Rm = st.number_input("Taxa com capitalização m (%):", value=10.0, step=0.1, key="Rm1") / 100
    m1 = st.number_input("Frequência m:", value=2, step=1, key="m1")
    Rc_calc = m1 * np.log(1 + Rm / m1)
    st.info(f"📉 Rc (contínua) ≈ {Rc_calc*100:.3f}% ao ano")

with col2:
    st.markdown("**➡️ De taxa contínua para capitalização m**")
    Rc = st.number_input("Taxa contínua (%):", value=8.0, step=0.1, key="Rc2") / 100
    m2 = st.number_input("Frequência m:", value=4, step=1, key="m2")
    Rm_calc = m2 * (np.exp(Rc / m2) - 1)
    st.info(f"📈 Rm (capitalizada) ≈ {Rm_calc*100:.3f}% ao ano")

st.divider()
st.caption("📚 Baseado no livro 'Opções, Futuros e Outros Derivativos', de John Hull")
