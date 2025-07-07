import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="📈 Duração e Convexidade")

st.title("📊 Duração e Convexidade de um Título")

st.markdown("""
Este app calcula a duração, convexidade e compara a estimativa de variação no preço de um título para mudanças na taxa de juros.
""")

# Input: Dados do título
st.header("Dados do título")
n = st.number_input("Número de fluxos de caixa (n)", min_value=1, value=6)
fluxos = []
tempos = []

st.write("Informe os fluxos de caixa ($) e os tempos (anos):")

for i in range(n):
    c = st.number_input(f"Fluxo de caixa c{i+1}", min_value=0.0, value=5.0 if i < n-1 else 105.0, step=0.1, format="%.2f")
    t = st.number_input(f"Tempo t{i+1} (anos)", min_value=0.0, value=0.5*(i+1), step=0.01, format="%.2f")
    fluxos.append(c)
    tempos.append(t)

fluxos = np.array(fluxos)
tempos = np.array(tempos)

# Input: rendimento atual (yield) contínuo composto
y = st.number_input("Rendimento anual (yield) com capitalização contínua (ex: 0.12 para 12%)", min_value=0.0, value=0.12, step=0.001, format="%.4f")

# Input: mudança na taxa
delta_y = st.number_input("Variação na taxa de juros (delta y) (ex: 0.001 para 0,1%)", value=0.001, step=0.0001, format="%.5f")

# Cálculos
pv_fluxos = fluxos * np.exp(-y * tempos)
B = np.sum(pv_fluxos)

# Duração
pesos = pv_fluxos / B
D = np.sum(pesos * tempos)

# Convexidade
Conv = np.sum(pesos * tempos**2)

# Estimativa de variação de preço pela duração (linear)
delta_B_dur = -B * D * delta_y

# Estimativa incluindo convexidade (quadrática)
delta_B_conv = delta_B_dur + 0.5 * B * Conv * delta_y**2

# Preços estimados após variação da taxa
B_apos_dur = B + delta_B_dur
B_apos_conv = B + delta_B_conv

# Output
st.header("Resultados")

st.write(f"**Preço atual do título:** ${B:.3f}")
st.write(f"**Duração:** {D:.4f} anos")
st.write(f"**Convexidade:** {Conv:.4f}")

st.write("---")

st.write(f"Estimativa de variação do preço com duração (linear): {delta_B_dur:.3f}")
st.write(f"Estimativa de variação do preço com duração + convexidade: {delta_B_conv:.3f}")

st.write(f"Preço estimado após variação da taxa (somente duração): ${B_apos_dur:.3f}")
st.write(f"Preço estimado após variação da taxa (duração + convexidade): ${B_apos_conv:.3f}")
