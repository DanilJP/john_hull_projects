import streamlit as st
import numpy as np

st.set_page_config(page_title="Calculadora de Duração de Título")

st.markdown("""
# 📉 Calculadora de Duração de Título

Calcule a duração de um título com base nos fluxos de caixa, seus tempos e rendimento (yield).

- O rendimento é usado para descontar os fluxos com capitalização contínua.
- A duração é a média ponderada dos tempos, ponderada pelo valor presente dos fluxos.
""")

# Inputs
n = st.number_input("Número de fluxos de caixa (n):", min_value=1, max_value=50, value=6, step=1)

# Entrada dos fluxos e tempos
cash_flows = []
times = []

st.markdown("### Insira os tempos (em anos) e fluxos de caixa correspondentes")

for i in range(n):
    t = st.number_input(f"Tempo t{i+1} (anos):", min_value=0.0, value=0.5*(i+1), step=0.01, key=f"time_{i}")
    c = st.number_input(f"Fluxo de caixa c{i+1} (valor):", min_value=0.0, value=5.0 if i < n-1 else 105.0, step=0.01, key=f"cf_{i}")
    times.append(t)
    cash_flows.append(c)

y = st.number_input("Rendimento anual contínuo (yield) [%]:", min_value=0.0, value=12.0, step=0.01) / 100

if st.button("Calcular Duração"):
    try:
        # Calcular preço do título
        valor_presente = [c * np.exp(-y * t) for c, t in zip(cash_flows, times)]
        B = sum(valor_presente)

        # Calcular duração
        D = sum(t * vp for t, vp in zip(times, valor_presente)) / B

        st.markdown(f"### Resultados:")
        st.write(f"Preço do título (B): {B:.3f}")
        st.write(f"Duração (anos): {D:.3f}")

    except Exception as e:
        st.error(f"Erro: {e}")
else:
    st.info("Insira os dados acima e clique em 'Calcular Duração'.")
