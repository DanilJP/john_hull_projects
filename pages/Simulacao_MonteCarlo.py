import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("🎲 Simulação Monte Carlo para MTM e PFE")

# Parâmetros
S0 = st.number_input("Preço inicial do ativo (S0)", value=100.0, step=1.0)
mu = st.number_input("Taxa de retorno esperada (mu) anual", value=0.05, step=0.01)
sigma = st.number_input("Volatilidade anual (sigma)", value=0.2, step=0.01)
T = st.number_input("Horizonte (anos)", value=1.0, step=0.1)
steps = st.number_input("Número de passos (intervalos de tempo)", value=252, step=1)
N = st.number_input("Número de simulações", value=1000, step=100)

# Definir posição/contrato simples: ex. posição longa 1 unidade do ativo
# Pode ser modificado para payoff de derivativos se quiser

if st.button("Rodar simulação"):

    dt = T / steps
    time_grid = np.linspace(0, T, steps + 1)

    # Simular preços com Geometric Brownian Motion
    # S(t+dt) = S(t)*exp((mu - 0.5*sigma^2)*dt + sigma*sqrt(dt)*Z)
    Z = np.random.normal(size=(N, steps))
    increments = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z
    log_S = np.cumsum(increments, axis=1)
    log_S = np.hstack([np.zeros((N,1)), log_S])  # Preço inicial no tempo 0
    S = S0 * np.exp(log_S)

    # MTM para posição linear (simples)
    # Suponha posição longa 1 ativo: MTM = preço do ativo (simplificação)
    MTM = S

    # Calcular PFE (ex: percentil 95 do MTM em cada tempo)
    pfe_95 = np.percentile(MTM, 95, axis=0)

    # Calcular MTM médio para plotar
    mtm_mean = np.mean(MTM, axis=0)

    # Plotar resultados
    fig, ax = plt.subplots(figsize=(10,6))
    # Plot algumas trajetórias (ex: 10)
    for i in range(min(10, N)):
        ax.plot(time_grid, MTM[i], color='gray', alpha=0.3)

    ax.plot(time_grid, mtm_mean, label='MTM Médio', color='blue', linewidth=2)
    ax.plot(time_grid, pfe_95, label='PFE 95%', color='red', linestyle='--', linewidth=2)
    ax.set_title("Simulação Monte Carlo de MTM e PFE")
    ax.set_xlabel("Tempo (anos)")
    ax.set_ylabel("MTM / Preço do ativo")
    ax.legend()
    st.pyplot(fig)

    # Mostrar tabela com MTM médio e PFE
    df_result = pd.DataFrame({
        "Tempo": time_grid,
        "MTM Médio": mtm_mean,
        "PFE 95%": pfe_95
    })
    st.write("Resumo dos resultados:")
    st.dataframe(df_result)
