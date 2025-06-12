# Calculadora de NDF Interativa com Streamlit
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Calculadora de NDF", layout="centered")

st.title("📈 Calculadora Interativa de NDF")

# Entradas do usuário
notional = st.number_input("Notional (USD)", min_value=1000, value=1_000_000, step=1000)
pre = st.number_input("Taxa Pré (anual)", min_value=0.0, max_value=1.0, value=0.15, step=0.01)
cupom = st.number_input("Cupom em USD (anual)", min_value=0.0, max_value=1.0, value=0.05, step=0.01)
spot = st.number_input("Spot atual (BRL/USD)", min_value=0.1, value=5.75, step=0.01)
data_ref = st.date_input("Data de referência", value=datetime(2025, 2, 19))
vencimento = st.date_input("Data de vencimento", value=datetime(2026, 2, 19))

# Lista de feriados nacionais (pode ser expandida)
brazil_holidays = [
    "2025-01-01", "2025-03-03", "2025-03-04", "2025-04-18", "2025-04-21",
    "2025-05-01", "2025-06-19", "2025-09-07", "2025-10-12", "2025-11-02",
    "2025-11-15", "2025-12-25", "2026-01-01", "2026-02-16", "2026-02-17",
    "2026-04-03", "2026-04-21", "2026-05-01", "2026-06-04", "2026-09-07",
    "2026-10-12", "2026-11-02", "2026-11-15", "2026-12-25"
]

def business_days_diff(start_date, end_date):
    return np.busday_count(
        np.datetime64(start_date.strftime("%Y-%m-%d")),
        np.datetime64(end_date.strftime("%Y-%m-%d")),
        holidays=brazil_holidays
    )

def diferenca_dias(data1, data2):
    return abs((data2 - data1).days)

# Cálculo dos dias úteis e corridos
ndu = business_days_diff(data_ref, vencimento)
ndc = diferenca_dias(data_ref, vencimento)

# Cálculo do Forward
fwd = spot * ((1 + pre)**(ndu / 252)) / (1 + cupom * ndc / 360)
fwd *= 0.98

st.markdown(f"**Forward calculado:** {fwd:.4f}")
st.markdown(f"**Dias úteis:** {ndu}, **Dias corridos:** {ndc}")

# Gráficos
valores_recebidos = []
spots_vencimento = []
valores_recebidos_ndf = []
spots_vencimento_ndf = []

range_min = st.slider("Spot mínimo para simulação", min_value=1.0, max_value=5.0, value=1.0, step=0.5)
range_max = st.slider("Spot máximo para simulação", min_value=6.0, max_value=15.0, value=9.0, step=0.5)

spot_range = np.arange(range_min, range_max + 1, 1)

for spot_vencimento in spot_range:
    valor_recebido = notional * (spot_vencimento - 5)
    valores_recebidos.append(valor_recebido)
    spots_vencimento.append(spot_vencimento)

    valor_recebido_ndf = notional * (fwd - spot_vencimento)
    valores_recebidos_ndf.append(valor_recebido_ndf)
    spots_vencimento_ndf.append(spot_vencimento)

# Payout total
payout_total = np.array(valores_recebidos) + np.array(valores_recebidos_ndf)

# Gráfico com matplotlib
fig, ax = plt.subplots()

ax.plot(spots_vencimento, valores_recebidos, marker='o', color="#1f77b4", linewidth=2, label='Fluxo 1 (exposição)')
ax.plot(spots_vencimento_ndf, valores_recebidos_ndf, marker='x', color="#ff7f0e", linewidth=2, label='NDF')
ax.plot(spots_vencimento_ndf, payout_total, marker='s', color="#2ca02c", linewidth=2, label='Payout total')

ax.set_xlabel('Spot no vencimento (BRL/USD)', fontsize=12)
ax.set_ylabel('Valor em BRL', fontsize=12)
ax.set_title('Spot vs. Valor Ajustado', fontsize=14, weight='bold', pad=15)

ax.legend(fontsize=10)
ax.grid(visible=True, alpha=0.3, linestyle="--")
ax.tick_params(colors='white', labelsize=10)
ax.spines['bottom'].set_color('gray')
ax.spines['left'].set_color('gray')

st.pyplot(fig)


# Tabela com os dados
import pandas as pd
df = pd.DataFrame({
    "Spot Vencimento": spot_range,
    "Fluxo 1 (exposição)": valores_recebidos,
    "NDF": valores_recebidos_ndf,
    "Payout Total": payout_total
})
st.dataframe(df.style.format({"Fluxo 1 (exposição)": "{:,.2f}", "NDF": "{:,.2f}", "Payout Total": "{:,.2f}"}))
