import streamlit as st
import numpy as np

st.title("🔮 Cálculo de PFE (Potential Future Exposure)")

num_simulacoes = st.number_input("Número de simulações Monte Carlo", min_value=1000, max_value=100000, value=10000, step=1000)
horizonte_dias = st.slider("Horizonte de cálculo (dias)", 1, 250, 30)

np.random.seed(42)
# Simulando variação de preço de ativo (GBM simplificado)
S0 = 100
mu = 0.05
sigma = 0.2

dt = 1 / 250
precos_futuros = S0 * np.exp(np.cumsum((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * np.random.randn(num_simulacoes, horizonte_dias), axis=1))

exposures = np.maximum(precos_futuros - S0, 0)  # Exposição positiva
pfe = np.percentile(exposures[:, -1], 95)  # percentil 95 do horizonte

st.write(f"PFE no horizonte de {horizonte_dias} dias (percentil 95): {pfe:.2f}")
st.line_chart(precos_futuros[:100].T)
