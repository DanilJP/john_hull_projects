# pages/7_Cross_Hedging.py
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from io import StringIO
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from utils.utils import css_utils

st.set_page_config(page_title="Cross Hedging — Variance-min hedge", layout="wide")

css_utils("Cross Hedging — Variance-min hedge")

# --------------- Example data (Hull table) ----------------
hull_table = pd.DataFrame({
    "month": list(range(1,16)),
    "deltaF": [0.021,0.035,-0.046,0.001,0.044,-0.029,-0.026,-0.029,0.048,-0.006,-0.036,-0.011,0.019,-0.027,0.029],
    "deltaS": [0.029,0.020,-0.044,0.008,0.026,-0.019,-0.010,-0.007,0.043,0.011,-0.036,-0.018,0.009,-0.032,0.023]
})

# --------------- Inputs: upload or use example ----------------
st.subheader("Problema :")
st.write('''Uma companhia aérea espera comprar 2 milhões de galões de combustível para aviação
em 1 mês e decide usar futuros de óleo para aquecimento para fins de hedge. Suponha
que a Tabela abaixo informa, para 15 meses sucessivos, dados sobre a mudança, DS, no
preço do combustível para aviação por galão e a mudança correspondente, DF, no preço
futuro para o contrato sobre óleo para aquecimento que seria usado para hedgear as mudanças de preço durante o mês.''')

st.subheader("1) Dados — Tabela com Preços e Futuros")
st.write("Abaixo os valores de ΔS e ΔF já calculados, indexados pelo mês.")

# use hull_table but treat as delta series
df = hull_table[["deltaS","deltaF"]].copy()

st.write("Amostra dos dados (primeiras linhas):")
st.dataframe(df.head())

st.markdown("_______", unsafe_allow_html=True)

# --------------- Parameters & position ---------------
st.subheader("2) Parâmetros & exposição")
col1, col2, col3 = st.columns([1.5,1,1])
with col1:
    qa_units = st.number_input("QA — exposição no ativo (unidades)", min_value=0.0, value=2000000.0, step=1.0, help="Ex: 2,000,000 galões (exemplo da companhia aérea)")
with col2:
    qf_units = st.number_input("QF — unidades por contrato futuro", min_value=1.0, value=42000.0, step=1.0, help="Unidades cobertas por 1 contrato futuro")
with col3:
    choose_method = st.selectbox("Método para N* (contratos)", ["usar QA/QF (unidades)", "usar valor monetário (VA/VF)"])
if choose_method == "usar valor monetário (VA/VF)":
    va = st.number_input("VA — valor monetário da exposição (USD)", value=2_000_000.0, step=1000.0)
    vf = st.number_input("VF — valor monetário por contrato (USD)", value=100_000.0, step=1000.0)
st.markdown("___", unsafe_allow_html=True)

# --------------- Compute metrics ---------------
st.subheader("3) Cálculos — h*, regressão e efetividade (R²)")

# compute stats on deltas
dS = df["deltaS"].astype(float).values
dF = df["deltaF"].astype(float).values

# sample statistics
sigma_S = np.std(dS, ddof=1)
sigma_F = np.std(dF, ddof=1)
cov = np.cov(dS, dF, ddof=1)[0,1]
rho = cov / (sigma_S * sigma_F) if sigma_S>0 and sigma_F>0 else np.nan

# h* formula
h_star = rho * (sigma_S / sigma_F) if sigma_F != 0 else np.nan

# regression ΔS = a + b ΔF  -> slope b is an estimate of h* (OLS)
model = LinearRegression().fit(dF.reshape(-1,1), dS.reshape(-1,1))
slope = float(model.coef_[0])
intercept = float(model.intercept_)
preds = model.predict(dF.reshape(-1,1)).ravel()
r2 = r2_score(dS, preds)

st.markdown("**Estatísticas amostrais**")
st.write({
    "sigma_S (std ΔS)": f"{sigma_S:.6f}",
    "sigma_F (std ΔF)": f"{sigma_F:.6f}",
    "cov(ΔS,ΔF)": f"{cov:.8f}",
    "rho (corr)": f"{rho:.4f}"
})

st.markdown("**Resultados**")
st.write(f"Razão de hedge de variância mínima (h*): **{h_star:.4f}**")
st.write(f"Estimativa via regressão (slope ΔS ~ ΔF): **{slope:.4f}** (intercept {intercept:.4f})")
st.write(f"Efetividade do hedge (R²): **{r2:.4f}**  — proporção da variância eliminada pelo hedge")

# --------------- Plot: scatter + regression ----------------
plot_df = pd.DataFrame({"deltaF": dF, "deltaS": dS, "pred": preds})
scatter = alt.Chart(plot_df).mark_circle(size=80).encode(
    x=alt.X('deltaF:Q', title='ΔF (change in future price)'),
    y=alt.Y('deltaS:Q', title='ΔS (change in spot price)'),
    tooltip=['deltaF','deltaS']
).properties(height=380, width='container')

reg_line = alt.Chart(pd.DataFrame({"deltaF":np.linspace(plot_df.deltaF.min(), plot_df.deltaF.max(), 100)})).mark_line(color='orange').encode(
    x='deltaF:Q',
    y=alt.Y('deltaF:Q', title='ΔS (pred line)', transform=None)
).transform_calculate(
    # custom predicted is slope*x + intercept
    pred = f"{intercept} + {slope} * datum.deltaF"
).encode(
    y='pred:Q'
)

# simpler: create line data
x_line = np.linspace(plot_df.deltaF.min(), plot_df.deltaF.max(), 100)
y_line = intercept + slope * x_line
line_df = pd.DataFrame({"deltaF": x_line, "pred": y_line})

reg_viz = alt.Chart(line_df).mark_line(color='orange').encode(x='deltaF:Q', y='pred:Q')

st.markdown("#### Scatter ΔS vs ΔF + linha de regressão")
st.altair_chart(scatter + reg_viz, use_container_width=True)

# --------------- Number of contracts N* ---------------
st.markdown("#### Número ideal de contratos (N*)")
if choose_method == "usar QA/QF (unidades)":
    N_star = (h_star * qa_units) / qf_units if (qf_units != 0 and not np.isnan(h_star)) else np.nan
    st.write(f"Com QA={qa_units:.0f} unidades e QF={qf_units:.0f} unidades/contrato → N* ≈ **{np.round(N_star,3)}** contratos")
else:
    N_star = (h_star * va) / vf if (vf != 0 and not np.isnan(h_star)) else np.nan
    st.write(f"Com VA={va:.2f} e VF={vf:.2f} → N* ≈ **{np.round(N_star,3)}** contratos (valor-monetário)")

# --------------- Table of metrics and download ---------------
res_table = {
    "sigma_S": [sigma_S],
    "sigma_F": [sigma_F],
    "rho": [rho],
    "h_star": [h_star],
    "reg_slope": [slope],
    "R2": [r2],
    "N_star": [N_star]
}
res_df = pd.DataFrame(res_table)
st.markdown("#### Resultados resumidos")
st.dataframe(res_df)

st.markdown("___", unsafe_allow_html=True)


