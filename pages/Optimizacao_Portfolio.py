import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import minimize

st.title("📈 Otimização de Portfólio")

np.random.seed(42)
# Simulando retornos esperados e covariância
n_ativos = st.slider("Número de ativos", 2, 10, 5)
retornos_esperados = np.random.uniform(0.01, 0.02, n_ativos)
cov = np.random.uniform(0.001, 0.005, (n_ativos, n_ativos))
cov = (cov + cov.T) / 2
np.fill_diagonal(cov, 0.01)

def fun_obj(x):
    return np.sqrt(np.dot(x.T, np.dot(cov, x)))  # Risco (desvio padrão)

constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
bounds = tuple((0,1) for _ in range(n_ativos))
x0 = np.ones(n_ativos) / n_ativos

resultado = minimize(fun_obj, x0, bounds=bounds, constraints=constraints)
pesos_otimos = resultado.x

df_result = pd.DataFrame({
    "Ativo": [f"Ativo {i+1}" for i in range(n_ativos)],
    "Peso Ótimo": pesos_otimos,
    "Retorno Esperado": retornos_esperados
})

st.write(df_result)
