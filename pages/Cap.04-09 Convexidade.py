import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="📈 Duração e Convexidade")

st.title("📊 Duração e Convexidade de um Título")

st.markdown("""
Este app calcula a duração, convexidade e compara a estimativa de variação no preço de um título para mudanças na taxa de juros.
""")

# Número de fluxos
n = st.number_input("Número de fluxos de caixa (n)", min_value=1, max_value=50, value=6)

# DataFrame editável
st.markdown("### Edite os fluxos de caixa e seus respectivos tempos:")

default_data = {
    "Tempo (anos)": [0.5 * (i + 1) for i in range(n)],
    "Fluxo de Caixa ($)": [5.0] * (n - 1) + [105.0]
}

df = pd.DataFrame(default_data)
edited_df = st.data_editor(df, num_rows="dynamic")

# Inputs da taxa de juros e variação
y = st.number_input("Rendimento anual (yield) com capitalização contínua (ex: 0.12 para 12%)", min_value=0.0, value=0.12, step=0.001, format="%.4f")
delta_y = st.number_input("Variação na taxa de juros (delta y) (ex: 0.001 para 0,1%)", value=0.001, step=0.0001, format="%.5f")

# Cálculos
tempos = edited_df["Tempo (anos)"].to_numpy()
fluxos = edited_df["Fluxo de Caixa ($)"].to_numpy()
pv_fluxos = fluxos * np.exp(-y * tempos)
B = np.sum(pv_fluxos)

pesos = pv_fluxos / B
D = np.sum(pesos * tempos)
Conv = np.sum(pesos * tempos**2)

# Estimativas
delta_B_dur = -B * D * delta_y
delta_B_conv = delta_B_dur + 0.5 * B * Conv * delta_y**2
B_apos_dur = B + delta_B_dur
B_apos_conv = B + delta_B_conv

# Resultados
st.header("Resultados")

st.write(f"**Preço atual do título:** ${B:.3f}")
st.write(f"**Duração:** {D:.4f} anos")
st.write(f"**Convexidade:** {Conv:.4f}")

st.write("---")

st.write(f"Estimativa de variação do preço com duração (linear): {delta_B_dur:.3f}")
st.write(f"Estimativa de variação do preço com duração + convexidade: {delta_B_conv:.3f}")

st.write(f"Preço estimado após variação da taxa (somente duração): ${B_apos_dur:.3f}")
st.write(f"Preço estimado após variação da taxa (duração + convexidade): ${B_apos_conv:.3f}")

# Gráfico de sensibilidade
st.header("📈 Sensibilidade do Preço ao Yield")

y_range = np.linspace(y - 0.02, y + 0.02, 100)
prices_exact = [np.sum(fluxos * np.exp(-yt * tempos)) for yt in y_range]
prices_dur = B - D * B * (y_range - y)
prices_conv = prices_dur + 0.5 * B * Conv * (y_range - y) ** 2

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(y_range * 100, prices_exact, label="Preço Exato", linewidth=2)
ax.plot(y_range * 100, prices_dur, "--", label="Aproximação (Duração)", linewidth=1.5)
ax.plot(y_range * 100, prices_conv, ":", label="Aproximação (Duração + Convexidade)", linewidth=1.5)

ax.set_xlabel("Yield (%)")
ax.set_ylabel("Preço do Título")
ax.set_title("Sensibilidade do Preço ao Yield")
ax.legend()
ax.grid(True)

st.pyplot(fig)
