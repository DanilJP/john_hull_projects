import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from pmdarima import auto_arima
from statsmodels.tsa.statespace.sarimax import SARIMAX

st.title("📈 Análise de Séries Temporais Financeiras com Previsão SARIMA")

# Gerar série de preços simulados
np.random.seed(42)
dias = pd.date_range(start='2023-01-01', periods=250)
retornos = np.random.normal(0, 0.01, 250)
precos = 100 * (1 + pd.Series(retornos)).cumprod()

df = pd.DataFrame({"Data": dias, "Preço": precos})
df.set_index("Data", inplace=True)

# Plot série histórica
fig1 = px.line(df, y="Preço", title="Preço Simulado")
st.plotly_chart(fig1)

st.write("Estatísticas básicas:")
st.write(df.describe())

# Previsão
st.markdown("---")
st.subheader("🔮 Previsão SARIMA")

n_periodos = st.slider("Escolha o número de dias para previsão", 7, 90, 30)

with st.spinner("Treinando modelo SARIMA..."):
    model_auto = auto_arima(df["Preço"], seasonal=True, m=5, suppress_warnings=True)
    model_sarima = SARIMAX(df["Preço"], order=model_auto.order, seasonal_order=model_auto.seasonal_order)
    model_fit = model_sarima.fit(disp=False)
    previsao = model_fit.get_forecast(steps=n_periodos)
    previsao_df = previsao.conf_int()
    previsao_df["Previsão"] = previsao.predicted_mean
    previsao_df.index = pd.date_range(df.index[-1] + pd.Timedelta(days=1), periods=n_periodos)

# Plot com previsão
df_previsao = pd.concat([df, previsao_df[["Previsão"]]], axis=0)

fig2 = px.line(df_previsao, y="Previsão", title="Previsão SARIMA")
fig2.add_scatter(x=df.index, y=df["Preço"], mode='lines', name='Histórico')

st.plotly_chart(fig2)

st.success("Previsão realizada com sucesso!")
