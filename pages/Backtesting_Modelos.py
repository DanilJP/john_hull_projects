import streamlit as st
import numpy as np
import pandas as pd

st.title("📊 Backtesting de Modelos Quantitativos")

np.random.seed(42)
# Simulação de sinais e retornos
dias = 250
retornos = np.random.normal(0, 0.01, dias)
sinais = np.random.choice([-1, 1], size=dias)

# Retorno do modelo
retorno_modelo = retornos * sinais
retorno_cumulativo = np.cumsum(retorno_modelo)

st.line_chart(retorno_cumulativo)
st.write("Retorno acumulado do modelo simulado.")
