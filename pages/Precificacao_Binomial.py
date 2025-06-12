import streamlit as st
import numpy as np

st.title("💹 Precificação Binomial de Opções")

def binomial_tree(S, K, T, r, sigma, steps, option_type="call"):
    dt = T / steps
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r*dt) - d) / (u - d)

    # Matriz do preço do ativo
    price = np.zeros((steps + 1, steps + 1))
    for i in range(steps + 1):
        for j in range(i + 1):
            price[j, i] = S * (u**(i-j)) * (d**j)

    # Matriz do valor da opção
    option = np.zeros_like(price)

    # Valor da opção no vencimento
    if option_type == "call":
        option[:, steps] = np.maximum(price[:, steps] - K, 0)
    else:
        option[:, steps] = np.maximum(K - price[:, steps], 0)

    # Retropropagação
    for i in range(steps - 1, -1, -1):
        for j in range(i + 1):
            option[j, i] = np.exp(-r*dt) * (p*option[j, i+1] + (1-p)*option[j+1, i+1])

    return option[0, 0]

S = st.number_input("Preço do ativo (S)", value=100.0)
K = st.number_input("Preço de exercício (K)", value=100.0)
T = st.number_input("Tempo até expiração (anos)", value=1.0)
r = st.number_input("Taxa livre de risco (r)", value=0.05)
sigma = st.number_input("Volatilidade (sigma)", value=0.2)
steps = st.number_input("Número de passos", min_value=1, max_value=1000, value=50)
option_type = st.selectbox("Tipo de opção", ["call", "put"])

if st.button("Calcular preço"):
    preco = binomial_tree(S, K, T, r, sigma, steps, option_type)
    st.write(f"Preço da opção {option_type}: {preco:.2f}")
