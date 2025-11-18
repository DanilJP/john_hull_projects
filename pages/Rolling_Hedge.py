# pages/Rolling_Hedge.py
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objs as go

from utils.utils import css_utils
css_utils("Rolagem de Hedge — Rolling Hedge")

st.set_page_config(page_title="Rolagem de Hedge — Rolling Hedge", layout="wide", initial_sidebar_state="collapsed")

# ------------------------------------------------------------
# HERO
# ------------------------------------------------------------
st.markdown('''#### Exemplo didático da rolagem de contratos futuros, baseado no Hull: P&L por roll, impacto no hedge e diferenças de fluxo de caixa.''')

st.markdown("______________________________________________________________", unsafe_allow_html=True)


# ------------------------------------------------------------
# 1) Introdução — O que é “rolar um hedge”
# ------------------------------------------------------------
st.subheader("1) O que é rolar um hedge?")
st.write("""
Quando uma empresa quer se proteger de um risco (ex.: queda do preço do petróleo),
mas **os contratos futuros disponíveis vencem antes do fim do horizonte de hedge**, ela precisa
**encerrar o contrato atual e abrir outro com vencimento mais distante**.

Isso se chama **rolagem (rolling)**.  
A operação típica é:

- Vender contrato futuro 1  
- Encerrar contrato futuro 1 e vender contrato futuro 2  
- Encerrar contrato futuro 2 e vender contrato futuro 3  
- ... até o final do horizonte  

Neste mini-projeto, vamos replicar exatamente o exemplo numérico do livro.
""")


st.markdown("______________________________________________________________", unsafe_allow_html=True)



# ------------------------------------------------------------
# 2) Dados fixos — exatamente como no exemplo do capítulo
# ------------------------------------------------------------
st.subheader("2) Dados da operação de rolagem")

exposure_units = 100_000          # exposição total
contract_size = 1_000             # cada contrato cobre 1k unidades
hedge_ratio = 1.0
initial_spot = 89.00
final_spot = 86.00

# Preços de venda e encerramento (3 rolls)
sell_prices  = [88.20, 87.00, 86.30]
close_prices = [87.40, 86.50, 85.90]

roll_labels = ["Out/14 → Enc.", "Mar/15 → Enc.", "Jul/15 → Enc."]

st.write(f"**Exposição protegida:** {exposure_units:,} unidades (ex.: barris)")
st.write(f"**Contrato futuro (tamanho):** {contract_size} unidades")
st.write(f"**Razão de hedge (h):** {hedge_ratio}")
st.write(f"**Preço à vista inicial:** {initial_spot} • **Preço à vista final:** {final_spot}")

df_rolls = pd.DataFrame({
    "Roll": roll_labels,
    "Preço Venda": sell_prices,
    "Preço Encerramento": close_prices,
})

df_rolls["Ganho por unidade"] = np.array(sell_prices) - np.array(close_prices)
df_rolls["Ganho total (R$)"] = df_rolls["Ganho por unidade"] * exposure_units

st.dataframe(df_rolls.head(3))


st.markdown("______________________________________________________________", unsafe_allow_html=True)



# ------------------------------------------------------------
# 3) P&L da estratégia de rolagem
# ------------------------------------------------------------
st.subheader("3) Resultado do hedge rolado")

total_gain_per_unit = df_rolls["Ganho por unidade"].sum()
total_gain = df_rolls["Ganho total (R$)"].sum()

spot_drop = initial_spot - final_spot   # queda do preço à vista
compensation_ratio = total_gain_per_unit / spot_drop

st.write(f"#### > Ganho total por unidade: **{total_gain_per_unit:.2f}**")
st.write(f"#### > Ganho total do hedge: **R$ {total_gain:,.2f}**")
st.write(f"#### > Queda no preço à vista: **{spot_drop:.2f}**")
st.write(f"#### > Compensação do hedge: **{compensation_ratio*100:.1f}% da queda**")

st.info(
    fr"""
Apesar da queda de **RS {spot_drop:.2f}**  no preço do ativo,
o hedge só compensou **RS {total_gain_per_unit:.2f}** por unidade — cerca de **{compensation_ratio*100:.1f}%**.

Isso ocorre porque:
- **Os contratos futuros estavam abaixo do preço à vista** (backwardation)
- Você só consegue garantir **o preço futuro**, não o preço spot
- A rolagem gera lucros pequenos repetidos, mas não cobre 100% da queda
"""
)



st.markdown("______________________________________________________________", unsafe_allow_html=True)



# ------------------------------------------------------------
# 4) Visualização — P&L acumulado por roll
# ------------------------------------------------------------
st.subheader("4) Visualização do P&L acumulado")

df_plot = pd.DataFrame({
    "Roll": ["Roll 1", "Roll 2", "Roll 3"],
    "Ganho Acumulado (por unidade)": np.cumsum(df_rolls["Ganho por unidade"])
})

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df_plot["Roll"],
    y=df_plot["Ganho Acumulado (por unidade)"],
    mode="lines+markers",
    line=dict(color="#4f46e5", width=3),
    marker=dict(size=8)
))

fig.update_layout(height=420, title="P&L acumulado a cada rolagem")
st.plotly_chart(fig, use_container_width=True)



st.markdown("______________________________________________________________", unsafe_allow_html=True)



# ------------------------------------------------------------
# 5) Explicação final — Por que entender rolagem importa?
# ------------------------------------------------------------
st.subheader("5) Conclusão — O que aprendemos")

st.write("""
Rolar um hedge parece simples, mas envolve pontos críticos:

### ✓ 1) Liquidez  
Nem sempre há contratos longos — por isso precisamos rolar.

### ✓ 2) Backwardation e Contango  
Se futuros estão **abaixo** do spot (backwardation), o hedge pode não compensar toda a queda.

### ✓ 3) Fluxo de caixa importa  
Mesmo lucrando no longo prazo, **as perdas de curto prazo nos ajustes diários podem quebrar uma empresa**
(se não houver caixa disponível).

Esse é exatamente o problema da **Metallgesellschaft**, mostrado no livro.
""")


st.markdown("______________________________________________________________", unsafe_allow_html=True)
