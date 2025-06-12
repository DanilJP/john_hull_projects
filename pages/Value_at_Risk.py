import streamlit as st
import numpy as np
import pandas as pd

st.title("📉 Cálculo de VaR (Value at Risk)")

# Dataset exemplo: simulação de retornos diários
np.random.seed(42)
retornos = np.random.normal(0, 0.01, 1000)  # 1000 dias de retorno
st.write("Exemplo de retornos diários simulados:")
st.line_chart(retornos)

nivel_confianca = st.slider("Nível de Confiança (%)", 90, 99, 95)
var = np.percentile(retornos, 100 - nivel_confianca)

st.write(f"VaR no nível de confiança de {nivel_confianca}% é aproximadamente: {abs(var):.4f}")
