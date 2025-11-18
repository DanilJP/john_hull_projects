# pages/Market_Price_of_Risk.py
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

from utils.utils import css_utils
css_utils("Market Price of Risk — λ")

st.set_page_config(page_title="Market Price of Risk (λ)", layout="wide", initial_sidebar_state="collapsed")

SEP = "______________________________________________________________"

# ---------- Hero ----------
st.markdown("""
### Entenda λ = (μ − r) / σ — como calcular, interpretar e ver efeitos em simulações (mundo real vs risk-neutral).
""", unsafe_allow_html=True)

st.markdown(SEP, unsafe_allow_html=True)

# ---------- 1) Definição rápida ----------
st.subheader("1) Definição curta")
st.write("""
O **preço de mercado do risco** (λ) para uma variável estocástica X relaciona o retorno excessivo esperado com a volatilidade:
**λ = (μ − r) / σ**.  
Isso significa que, para derivativos que dependem apenas de X, o prêmio de risco por unidade de volatilidade é comum (sem arbitragem).
Em particular, no **mundo risk-neutral** λ = 0 e o drift efetivo dos ativos é a taxa livre de risco r.
""")

st.markdown(SEP, unsafe_allow_html=True)

# ---------- 2) Controles: parâmetros e exemplos ----------
st.subheader("2) Parâmetros e exemplos (calcule λ)")

c1, c2, c3 = st.columns(3)
with c1:
    r = st.number_input("Taxa livre de risco r (a.a.)", value=0.08, format="%.4f", step=0.01)
    mu = st.number_input("Retorno esperado do derivativo μ (a.a.)", value=0.12, format="%.4f", step=0.01)
with c2:
    sigma = st.number_input("Volatilidade σ do derivativo (a.a.)", value=0.20, format="%.4f", step=0.01)
    name = st.text_input("Nome do ativo/derivativo (ex.: opção sobre petróleo)", value="f")
with c3:
    simulate_n = st.slider("Nº de caminhos para simulação", min_value=100, max_value=5000, value=1000, step=100)
    days = st.slider("Horizonte (dias úteis)", min_value=30, max_value=252, value=252, step=1)

if st.button("Calcular λ e simular"):
    lam = (mu - r) / sigma if sigma != 0 else np.nan
    st.session_state["mpr"] = {"r": r, "mu": mu, "sigma": sigma, "lambda": lam}
    st.success(f"λ calculado: {lam:.4f}")

# quick examples (based on chapter examples)
st.markdown("**Exemplos rápidos (capítulo):**")
st.write("- Exemplo: derivativo com μ=12%, σ=20%, r=8% → λ = (0.12−0.08)/0.20 = 0.20")
st.write("- Se λ=0 → mundo risk-neutral, drift = r")

st.markdown(SEP, unsafe_allow_html=True)

# ---------- 3) Simulação: mundo real vs risk-neutral ----------
st.subheader("3) Simulação: caminhos GBM — Mundo real vs Risk-neutral")

def simulate_gbm(S0, mu, sigma, days, n_paths, seed=42):
    np.random.seed(seed)
    dt = 1/252
    steps = days
    shape = (n_paths, steps+1)
    paths = np.zeros(shape)
    paths[:,0] = S0
    for t in range(1, steps+1):
        z = np.random.normal(size=n_paths)
        paths[:,t] = paths[:,t-1] * np.exp((mu - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*z)
    return paths

if "mpr" in st.session_state:
    params = st.session_state["mpr"]
    S0 = 100.0
    # real-world drift = mu (user input)
    paths_real = simulate_gbm(S0, params["mu"], params["sigma"], days, simulate_n)
    # risk-neutral drift = r
    paths_rn = simulate_gbm(S0, params["r"], params["sigma"], days, simulate_n)

    # build summary stats: expected terminal price
    term_real = paths_real[:,-1]
    term_rn = paths_rn[:,-1]
    mean_real = np.mean(term_real)
    mean_rn = np.mean(term_rn)

    st.write(f"- Valor esperado no mundo real (μ): {mean_real:.2f}")
    st.write(f"- Valor esperado no mundo risk-neutral (r): {mean_rn:.2f}")
    st.write(f"- λ = {params['lambda']:.4f}")

    # prepare data for plotting density of terminal distribution
    df_plot = pd.DataFrame({
        "terminal_real": term_real,
        "terminal_rn": term_rn
    })

    # density charts with Altair
    df_melt = df_plot.melt(var_name="scenario", value_name="terminal_price")
    chart = alt.Chart(df_melt).transform_density(
        "terminal_price",
        as_=["terminal_price", "density"],
        groupby=["scenario"],
    ).mark_area(opacity=0.5).encode(
        x=alt.X("terminal_price:Q", title="Preço terminal"),
        y="density:Q",
        color="scenario:N"
    ).properties(height=320)
    st.altair_chart(chart, use_container_width=True)

    st.markdown(SEP, unsafe_allow_html=True)

    # time series small sample
    sample_idx = np.random.choice(simulate_n, size=min(6, simulate_n), replace=False)
    df_ts = pd.DataFrame({
        "time": np.arange(days+1)
    })
    for i, idx in enumerate(sample_idx):
        df_ts[f"real_{i}"] = paths_real[idx,:]
        df_ts[f"rn_{i}"] = paths_rn[idx,:]

    df_ts_melt = df_ts.melt(id_vars="time", var_name="path", value_name="price")
    chart2 = alt.Chart(df_ts_melt).mark_line(opacity=0.8).encode(
        x="time:Q",
        y="price:Q",
        color="path:N"
    ).properties(height=320)
    st.altair_chart(chart2, use_container_width=True)

else:
    st.info("Calcule λ e simule (botão 'Calcular λ e simular').")

st.markdown(SEP, unsafe_allow_html=True)

# ---------- 4) Multiderivativos: mesma λ, retornos diferentes ----------
st.subheader("4) Preço de mercado do risco é único para a variável X")

st.write("""
Se f1 e f2 dependem apenas da mesma variável X, então (sem arbitragem) ambos têm o mesmo λ = (μ − r) / σ_Xf,
ou seja, o preço de mercado do risco por unidade de volatilidade é comum — diferente volatilidade implica retorno exigido proporcional.
""")

# quick calculator: given lambda and sigma of asset2 compute implied mu2
col_a, col_b = st.columns([1,1])
with col_a:
    use_lambda = st.number_input("Use um λ fixo (opcional)", value=0.20, format="%.4f")
    sigma2 = st.number_input("σ do segundo derivativo (a.a.)", value=0.30, format="%.4f")
with col_b:
    implied_mu2 = st.number_input("Resultado: μ₂ implícito (se usar λ)", value=(r + use_lambda * sigma2), format="%.4f", disabled=True)
st.write(f"Se λ={use_lambda:.3f} e σ₂={sigma2:.3f} então μ₂ = r + λ·σ₂ = {implied_mu2:.3f}")

