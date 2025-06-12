import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Melhor configuração para visualização mobile
st.set_page_config(page_title="Análise de Crédito", layout="centered")

st.title("🔍 Análise de Crédito")
st.markdown("""
Simulação de análise de risco de crédito para identificar padrões relacionados à inadimplência.

- Dados simulados
- Visualizações compactas
- Foco em usabilidade mobile 📱
""")

# --- Dataset Simulado ---
@st.cache_data
def criar_dataset():
    return pd.DataFrame({
        "idade": [25, 45, 35, 50, 23, 40, 60, 37, 48, 33],
        "renda_mensal": [3000, 8000, 5000, 10000, 2500, 7000, 12000, 5200, 7800, 4800],
        "score_credito": [600, 720, 680, 730, 590, 710, 750, 690, 720, 670],
        "inadimplente": [0, 0, 0, 0, 1, 0, 0, 1, 0, 1]
    })

df = criar_dataset()

# --- Visualização compacta dos dados ---
with st.expander("📄 Ver dados"):
    st.dataframe(df, use_container_width=True, height=200)

# --- Filtros simples para celular ---
filtro = st.radio("Filtrar clientes:", ["Todos", "Inadimplentes", "Adimplentes"], horizontal=True)
df_filtrado = df.copy()

if filtro == "Inadimplentes":
    df_filtrado = df[df["inadimplente"] == 1]
elif filtro == "Adimplentes":
    df_filtrado = df[df["inadimplente"] == 0]

# --- Gráficos interativos e pequenos ---
st.subheader("📊 Análises Visuais")

if st.checkbox("🔢 Distribuição"):
    fig, ax = plt.subplots(figsize=(3.5, 2.5))
    sns.countplot(x="inadimplente", data=df_filtrado, ax=ax, palette="Set2")
    ax.set_xticklabels(["Adimplente", "Inadimplente"])
    ax.set_title("Distribuição")
    st.pyplot(fig, use_container_width=True)

if st.checkbox("📦 Boxplot"):
    coluna = st.selectbox("Variável:", ["idade", "renda_mensal", "score_credito"])
    fig, ax = plt.subplots(figsize=(3.5, 2.5))
    sns.boxplot(x="inadimplente", y=coluna, data=df_filtrado, palette="Set3", ax=ax)
    ax.set_xticklabels(["Adimplente", "Inadimplente"])
    ax.set_title(f"{coluna.replace('_', ' ').title()}")
    st.pyplot(fig, use_container_width=True)

if st.checkbox("📌 Correlação"):
    fig, ax = plt.subplots(figsize=(3.5, 2.8))
    sns.heatmap(df_filtrado.corr(), annot=True, cmap="coolwarm", ax=ax, fmt=".2f")
    ax.set_title("Correlação")
    st.pyplot(fig, use_container_width=True)

# --- Insight simples e direto ---
if st.checkbox("🧠 Insight rápido"):
    inad_pct = df["inadimplente"].mean() * 100
    st.markdown(f"📉 Taxa de inadimplência geral: **{inad_pct:.1f}%**")
    st.markdown("Clientes inadimplentes tendem a ter score mais baixo.")

# --- Rodapé ---
st.markdown("---")
st.markdown("<center><small>Projeto de Estudo • Daniel Juliano</small></center>", unsafe_allow_html=True)
