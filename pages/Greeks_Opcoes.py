import streamlit as st
import numpy as np
import scipy.stats as si

st.title("💹 Cálculo dos Greeks para Opções")

def black_scholes_greeks(S, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2)*T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    delta = si.norm.cdf(d1) if option_type == "call" else -si.norm.cdf(-d1)
    gamma = si.norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * si.norm.pdf(d1) * np.sqrt(T)
    theta = None
    if option_type == "call":
        theta = (-S * si.norm.pdf(d1) * sigma / (2 * np.sqrt(T)) -
                 r * K * np.exp(-r * T) * si.norm.cdf(d2))
    else:
        theta = (-S * si.norm.pdf(d1) * sigma / (2 * np.sqrt(T)) +
                 r * K * np.exp(-r * T) * si.norm.cdf(-d2))
    rho = K * T * np.exp(-r * T) * si.norm.cdf(d2) if option_type == "call" else -K * T * np.exp(-r * T) * si.norm.cdf(-d2)

    return delta, gamma, vega, theta, rho

S = st.number_input("Preço do ativo (S)", value=100.0)
K = st.number_input("Preço de exercício (K)", value=100.0)
T = st.number_input("Tempo até expiração (anos)", value=1.0)
r = st.number_input("Taxa livre de risco (r)", value=0.05)
sigma = st.number_input("Volatilidade (sigma)", value=0.2)
option_type = st.selectbox("Tipo de opção", ["call", "put"])

if st.button("Calcular Greeks"):
    delta, gamma, vega, theta, rho = black_scholes_greeks(S, K, T, r, sigma, option_type)
    st.write(f"Delta: {delta:.4f}")
    st.write(f"Gamma: {gamma:.4f}")
    st.write(f"Vega: {vega:.4f}")
    st.write(f"Theta: {theta:.4f}")
    st.write(f"Rho: {rho:.4f}")
