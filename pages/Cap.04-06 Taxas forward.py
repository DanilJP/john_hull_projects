import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Calculadora de Taxas Forward", layout="centered")

st.markdown("""
# 📈 Calculadora de Taxas Forward

Com base nas taxas zero para diferentes vencimentos, esta calculadora estima as taxas forward entre períodos consecutivos usando capitalização contínua.

### Fórmula da taxa forward entre \(T_1\) e \(T_2\):

\[
R_F = \frac{R_2 T_2 - R_1 T_1}{T_2 - T_1}
\]

---

### Insira as taxas zero (em % ao ano) e seus vencimentos (anos):
""")

# Entradas
vencimentos = st.text_input("Vencimentos (anos), separados por vírgula:", "1, 2, 3, 4, 5")
taxas_zero_str = st.text_input("Taxas zero (% ao ano), separadas por vírgula:", "3.0, 4.0, 4.6, 5.0, 5.3")

if st.button("Calcular taxas forward"):
    try:
        # Processa entradas
        T = np.array([float(x.strip()) for x in vencimentos.split(",")])
        R = np.array([float(x.strip()) / 100 for x in taxas_zero_str.split(",")])  # convertendo para decimal

        if len(T) != len(R):
            st.error("Número de vencimentos e taxas zero deve ser igual.")
        else:
            # Calcular taxas forward para cada intervalo entre vencimentos
            forward_rates = []
            for i in range(1, len(T)):
                RF = (R[i]*T[i] - R[i-1]*T[i-1]) / (T[i] - T[i-1])
                forward_rates.append(RF)

            # Mostrar resultados
            df = pd.DataFrame({
                "Período (anos)": [f"{T[i-1]} a {T[i]}" for i in range(1, len(T))],
                "Taxa Forward (%)": [f"{rf*100:.3f}" for rf in forward_rates]
            })
            st.markdown("### Resultados das taxas forward entre períodos")
            st.dataframe(df)

            # Mostrar taxa forward instantânea aproximada via derivada numérica
            st.markdown("---")
            st.markdown("### Taxa forward instantânea aproximada")

            # Derivada numérica simples para taxa forward instantânea
            dT = np.diff(T)
            dRT = np.diff(R*T)
            forward_instantanea = dRT / dT
            T_mid = (T[:-1] + T[1:]) / 2

            df_inst = pd.DataFrame({
                "Tempo (anos)": [f"{t:.2f}" for t in T_mid],
                "Taxa Forward Instantânea (%)": [f"{rf*100:.3f}" for rf in forward_instantanea]
            })
            st.dataframe(df_inst)

    except Exception as e:
        st.error(f"Erro no processamento: {e}")

else:
    st.info("Preencha os campos acima e clique em 'Calcular taxas forward'.")
