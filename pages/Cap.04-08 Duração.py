import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Calculadora de Duração de Título")

st.markdown("""
# 📉 Calculadora de Duração de Título

Calcule a duração de um título com base nos fluxos de caixa, seus tempos e rendimento (yield).

- O rendimento é usado para descontar os fluxos com capitalização contínua.
- A duração é a média ponderada dos tempos, ponderada pelo valor presente dos fluxos.
""")

# Inputs
n = st.number_input("Número de fluxos de caixa (n):", min_value=1, max_value=50, value=6, step=1)

# Criar DataFrame inicial
default_data = {
    "Tempo (anos)": [0.5*(i+1) for i in range(n)],
    "Fluxo de Caixa": [5.0]*(n-1) + [105.0]
}
df = pd.DataFrame(default_data)

# Editor de DataFrame
st.markdown("### Edite os valores abaixo:")
edited_df = st.data_editor(df, num_rows="dynamic")

# Entrada do rendimento
y = st.number_input("Rendimento anual contínuo (yield) [%]:", min_value=0.0, value=12.0, step=0.01) / 100

# Calcular
if st.button("Calcular Duração"):
    try:
        times = edited_df["Tempo (anos)"].to_numpy()
        cash_flows = edited_df["Fluxo de Caixa"].to_numpy()

        # Calcular preço do título
        valor_presente = cash_flows * np.exp(-y * times)
        B = valor_presente.sum()

        # Calcular duração
        D = (times * valor_presente).sum() / B

        st.markdown(f"### Resultados:")
        st.write(f"Preço do título (B): {B:.3f}")
        st.write(f"Duração (anos): {D:.3f}")

    except Exception as e:
        st.error(f"Erro: {e}")
else:
    st.info("Edite os dados acima e clique em 'Calcular Duração'.")
