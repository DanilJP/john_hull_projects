import streamlit as st
import pandas as pd
import numpy as np

# Configuração visual
st.set_page_config(page_title="Projetos Quant")
st.markdown("<h1 style='text-align: left;'>💼 Calculadora de Probabilidade de Inadimplência</h1>", unsafe_allow_html=True)

# Dados da tabela
data = {
    1:   [0.000, 0.022, 0.063, 0.177, 1.112, 4.051, 16.448],
    2:   [0.013, 0.069, 0.203, 0.495, 3.083, 9.608, 27.867],
    3:   [0.013, 0.139, 0.414, 0.894, 5.424, 15.216, 36.908],
    4:   [0.037, 0.256, 0.625, 1.369, 7.934, 20.134, 44.128],
    5:   [0.106, 0.383, 0.870, 1.877, 10.189, 24.613, 50.366],
    7:   [0.247, 0.621, 1.441, 2.927, 14.117, 32.747, 58.302],
    10:  [0.503, 0.922, 2.480, 4.740, 19.708, 41.947, 69.483],
    15:  [0.935, 1.756, 4.255, 8.628, 29.172, 52.217, 79.178],
    20:  [1.104, 3.135, 6.841, 12.483, 36.321, 58.084, 81.248],
}
ratings = ["Aaa", "Aa", "A", "Baa", "Ba", "B", "Caa–C"]
df = pd.DataFrame(data, index=ratings)
df.columns.name = "Termo (anos)"
df.index.name = "Rating"

# Mostrar tabela
st.markdown("#### 📊 Tabela de Probabilidade Cumulativa de Inadimplência (%)")
st.dataframe(df.style.format("{:.3f}"), use_container_width=True)

# Interface interativa
st.markdown("---")
st.markdown("### 🔍 Escolha Rating e Prazo para Análise")

col1, col2 = st.columns(2)
rating_escolhido = col1.selectbox("Escolha o rating", ratings)
prazo_escolhido = col2.number_input("Digite o prazo (anos)", min_value=0.5, step=0.5, value=5.0)

# Buscar valor da tabela
prob_percent = np.interp(
    prazo_escolhido,
    sorted(df.columns),
    df.loc[rating_escolhido].values
)
prob = prob_percent / 100

# Cálculo de lambda (fator de risco)
if prob < 1.0:
    lambda_calc = -np.log(1 - prob) / prazo_escolhido
else:
    lambda_calc = float('inf')

# Resultados
st.markdown(f"### 📈 Resultado para Rating **{rating_escolhido}** e Prazo **{prazo_escolhido} anos**")
st.info(f"Probabilidade de inadimplência da tabela: **{prob_percent:.3f}%**")

if lambda_calc != float('inf'):
    st.success(f"Fator de risco implícito estimado (λ): **{lambda_calc:.4f}**")

    with st.expander("🧮 Cálculo detalhado passo a passo"):
        ln_term = np.log(1 - prob)
        st.markdown(f"""
**Passo a passo do cálculo:**

1. Probabilidade decimal P(t):
   {prob:.5f}

2. Cálculo do logaritmo natural:
   ln(1 - P(t)) = ln(1 - {prob:.5f}) = {ln_term:.5f}

3. Negar o valor do logaritmo:
   -ln(1 - P(t)) = {-ln_term:.5f}

4. Dividir pelo prazo t (anos):
   λ = (-ln(1 - P(t))) / t = {-ln_term:.5f} / {prazo_escolhido} = {lambda_calc:.5f}
""")
else:
    st.warning("Probabilidade de 100%. Não é possível calcular λ com essa fórmula.")
