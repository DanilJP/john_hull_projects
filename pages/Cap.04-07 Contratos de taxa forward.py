import streamlit as st
import numpy as np

st.set_page_config(page_title="Calculadora de Valor FRA")

st.markdown("""
# 💼 Calculadora de Valor de Contrato FRA

Calcule o valor presente de um Contrato de Taxa Forward (FRA) baseado em:

- Principal \(L\)
- Taxa fixa acordada \(R_K\)
- Taxa forward LIBOR esperada \(R_F\) (pressuposta como taxa realizada \(R_M\))
- Período do contrato (de \(T_1\) até \(T_2\))
- Taxa zero livre de risco \(R_2\) para o vencimento \(T_2\)

Todas as taxas devem estar na mesma frequência de capitalização (ex: semestral, trimestral).
""")

# Inputs
principal = st.number_input("Principal (L) em unidades monetárias:", min_value=0.0, value=100_000_000.0, step=1_000_000.0, format="%f")
RK = st.number_input("Taxa fixa acordada no FRA (R_K) [% ao ano]:", min_value=0.0, value=4.0, step=0.01) / 100
RF = st.number_input("Taxa forward LIBOR esperada (R_F) [% ao ano]:", min_value=0.0, value=5.0, step=0.01) / 100
T1 = st.number_input("Início do período do empréstimo (T1) em anos:", min_value=0.0, value=1.5, step=0.01)
T2 = st.number_input("Fim do período do empréstimo (T2) em anos:", min_value=0.0, value=2.0, step=0.01)
R2 = st.number_input("Taxa zero livre de risco para vencimento T2 (R2) [% ao ano, contínua]:", min_value=0.0, value=4.0, step=0.01) / 100

if st.button("Calcular Valor do FRA"):
    try:
        delta_T = T2 - T1
        if delta_T <= 0:
            st.error("Erro: T2 deve ser maior que T1.")
        else:
            # Valor do FRA (pressupondo R_M = R_F)
            valor_fra_T2 = principal * (RK - RF) * delta_T  # valor no tempo T2
            valor_fra_T1 = valor_fra_T2 * np.exp(-R2 * T2)  # descontado para T1

            st.markdown(f"### Resultados:")
            st.write(f"Valor do FRA no tempo T2: {valor_fra_T2:,.2f}")
            st.write(f"Valor presente do FRA no tempo T1 (descontado pela taxa zero): {valor_fra_T1:,.2f}")

    except Exception as e:
        st.error(f"Erro: {e}")

else:
    st.info("Preencha os parâmetros acima e clique em 'Calcular Valor do FRA'.")
