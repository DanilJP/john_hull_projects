import streamlit as st
import numpy as np
from scipy.stats import norm

st.title("📈 Precificação de Opções - Black-Scholes")

def black_scholes(S, K, T, r, sigma, tipo):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    if tipo == 'call':
        return S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
    else:
        return K * np.exp(-r*T) * norm.cdf(-d2) - S * norm.cdf(-d1)

S = st.number_input("Preço do ativo (S)", value=100.0)
K = st.number_input("Preço de exercício (K)", value=100.0)
T = st.number_input("Tempo até o vencimento (T, em anos)", value=1.0)
r = st.number_input("Taxa de juros (r)", value=0.05)
sigma = st.number_input("Volatilidade (sigma)", value=0.2)
tipo = st.selectbox("Tipo de opção", ['call', 'put'])

if st.button("Calcular preço"):
    preco = black_scholes(S, K, T, r, sigma, tipo)
    st.success(f"Preço da opção {tipo}: R$ {preco:.2f}")

