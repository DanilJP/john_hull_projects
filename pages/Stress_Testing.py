import streamlit as st
import numpy as np
import pandas as pd

st.title("⚠️ Stress Testing para Carteiras")

# Exemplo simples: choque nos retornos
choque = st.slider("Choque negativo nos retornos (%)", 1, 20, 5)

np.random.seed(42)
retornos = np.random.normal(0, 0.01, 1000)
retornos_choque = retornos - (choque / 100)

st.write("Retornos originais:")
st.line_chart(retornos)
st.write(f"Retornos após choque de {choque}%:")
st.line_chart(retornos_choque)

impacto = np.mean(retornos_choque) - np.mean(retornos)
st.write(f"Impacto médio do choque na carteira: {impacto:.4f}")
