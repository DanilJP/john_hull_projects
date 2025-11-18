# pages/Market_Price_of_Risk.py
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objs as go

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
O **preço de mercado do risco** (λ) para uma variável X relaciona o retorno excessivo esperado com a volatilidade:
**λ = (μ − r) / σ**.  
No **mundo risk-neutral** λ = 0 e o drift efetivo dos ativos é a taxa livre de risco _r_.
""")
st.markdown(SEP, unsafe_allow_html=True)

# ---------- 2) Controles: parâmetros e exemplos ----------
st.subheader("2) Parâmetros e cálculo de λ")

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

calc_clicked = st.button("Calcular λ e simular")

if calc_clicked:
    lam = (mu - r) / sigma if sigma != 0 else np.nan
    st.session_state["mpr"] = {"r": r, "mu": mu, "sigma": sigma, "lambda": lam}
    st.success(f"λ calculado: {lam:.4f}")

st.markdown("**Exemplo:** μ=12%, σ=20%, r=8% → λ = 0.20")
st.markdown(SEP, unsafe_allow_html=True)

# ---------- 3) Simulação: mundo real vs risk-neutral ----------
st.subheader("3) Simulação: caminhos GBM — Mundo real vs Risk-neutral")

def simulate_gbm(S0, mu, sigma, days, n_paths, seed=42):
    np.random.seed(seed)
    dt = 1/252
    steps = days
    paths = np.zeros((n_paths, steps+1))
    paths[:,0] = S0
    for t in range(1, steps+1):
        z = np.random.normal(size=n_paths)
        paths[:,t] = paths[:,t-1] * np.exp((mu - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*z)
    return paths

def compute_density(xs, samples):
    """Try gaussian_kde; fallback to histogram+interp."""
    try:
        from scipy.stats import gaussian_kde
        kde = gaussian_kde(samples)
        return kde(xs)
    except Exception:
        # fallback: histogram -> density -> interp
        hist, bin_edges = np.histogram(samples, bins=80, density=True)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        dens = np.interp(xs, bin_centers, hist)
        # small smoothing via convolution (simple)
        dens = np.convolve(dens, np.ones(3)/3, mode='same')
        return dens

if "mpr" in st.session_state:
    params = st.session_state["mpr"]
    S0 = 100.0
    paths_real = simulate_gbm(S0, params["mu"], params["sigma"], days, simulate_n)
    paths_rn   = simulate_gbm(S0, params["r"], params["sigma"], days, simulate_n)

    term_real = paths_real[:,-1]
    term_rn   = paths_rn[:,-1]
    mean_real = np.mean(term_real)
    mean_rn   = np.mean(term_rn)

    st.write(f"- Valor esperado (mundo real, μ): {mean_real:.2f}")
    st.write(f"- Valor esperado (risk-neutral, r): {mean_rn:.2f}")
    st.write(f"- λ = {params['lambda']:.4f}")

    # DENSITY PLOT (Plotly)
    all_min = min(term_real.min(), term_rn.min())
    all_max = max(term_real.max(), term_rn.max())
    xs = np.linspace(all_min*0.9, all_max*1.1, 300)
    dens_real = compute_density(xs, term_real)
    dens_rn   = compute_density(xs, term_rn)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=dens_real, name="Terminal (mundo real, μ)", fill='tozeroy',
                             mode='lines', line=dict(color='#1f77b4'), opacity=0.6))
    fig.add_trace(go.Scatter(x=xs, y=dens_rn, name="Terminal (risk-neutral, r)", fill='tozeroy',
                             mode='lines', line=dict(color='#ff7f0e'), opacity=0.6))
    # vertical lines for means
    fig.add_vline(x=mean_real, line=dict(color='#1f77b4', dash='dash'), annotation_text=f"μ mean {mean_real:.1f}", annotation_position="top left")
    fig.add_vline(x=mean_rn, line=dict(color='#ff7f0e', dash='dash'), annotation_text=f"r mean {mean_rn:.1f}", annotation_position="top right")

    fig.update_layout(
        title="Densidade do preço terminal — Mundo real vs Risk-neutral",
        xaxis_title="Preço terminal",
        yaxis_title="Densidade",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=420,
        margin=dict(l=40, r=20, t=60, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Interpretação rápida:** as duas curvas têm mesma dispersão (σ), mas médias deslocadas — no mundo real o drift é μ; no risk-neutral é r (λ captura esse deslocamento).", unsafe_allow_html=True)
    st.markdown(SEP, unsafe_allow_html=True)

    # TIME SERIES SAMPLE (Plotly)
    st.subheader("Amostra de caminhos (exemplos) — destaque para a média")
    sample_idx = np.random.choice(simulate_n, size=min(6, simulate_n), replace=False)
    fig2 = go.Figure()
    # plot individual real-world paths (faint)
    for i, idx in enumerate(sample_idx):
        fig2.add_trace(go.Scatter(x=np.arange(days+1), y=paths_real[idx,:], mode='lines',
                                  name=f"real_{i+1}", line=dict(color='rgba(31,119,180,0.25)'), showlegend=False))
    # plot individual risk-neutral paths (faint)
    for i, idx in enumerate(sample_idx):
        fig2.add_trace(go.Scatter(x=np.arange(days+1), y=paths_rn[idx,:], mode='lines',
                                  name=f"rn_{i+1}", line=dict(color='rgba(255,127,14,0.25)'), showlegend=False))
    # plot mean lines
    mean_real_ts = np.mean(paths_real, axis=0)
    mean_rn_ts   = np.mean(paths_rn, axis=0)
    fig2.add_trace(go.Scatter(x=np.arange(days+1), y=mean_real_ts, mode='lines', name='Mean (μ)', line=dict(color='#1f77b4', width=3)))
    fig2.add_trace(go.Scatter(x=np.arange(days+1), y=mean_rn_ts, mode='lines', name='Mean (r)', line=dict(color='#ff7f0e', width=3)))
    fig2.update_layout(title="Caminhos de preços (exemplos) — médias destacadas",
                       xaxis_title="Dias",
                       yaxis_title="Preço",
                       height=420,
                       margin=dict(l=40, r=20, t=60, b=40),
                       legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig2, use_container_width=True)

else:
    st.info("Calcule λ e simule (botão 'Calcular λ e simular').")

st.markdown(SEP, unsafe_allow_html=True)

# ---------- 4) Multiderivativos: mesma λ, retornos diferentes ----------
st.subheader("4) Preço de mercado do risco é único para a variável X")
st.write("""
Se f1 e f2 dependem apenas da mesma variável X, então (sem arbitragem) ambos têm o mesmo λ = (μ − r) / σ_Xf.
Assim, variáveis com volatilidades diferentes exigem retornos esperados proporcionais (μ = r + λ·σ).
""")

col_a, col_b = st.columns([1,1])
with col_a:
    use_lambda = st.number_input("Use um λ fixo (opcional)", value=0.20, format="%.4f")
    sigma2 = st.number_input("σ do segundo derivativo (a.a.)", value=0.30, format="%.4f")
with col_b:
    implied_mu2 = r + use_lambda * sigma2
    st.number_input("Resultado: μ₂ implícito (se usar λ)", value=float(implied_mu2), format="%.4f", disabled=True)

st.markdown(SEP, unsafe_allow_html=True)

