import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

st.title("💳 Modelagem de Risco de Crédito")

def criar_dataset():
    data = {
        "idade": [25, 45, 35, 50, 23, 40, 60, 37, 48, 33],
        "renda_mensal": [3000, 8000, 5000, 10000, 2500, 7000, 12000, 5200, 7800, 4800],
        "score_credito": [600, 720, 680, 730, 590, 710, 750, 690, 720, 670],
        "inadimplente": [0, 0, 0, 0, 1, 0, 0, 1, 0, 1]
    }
    return pd.DataFrame(data)

# Inicializa o dataset no session_state
if "dataset" not in st.session_state:
    st.session_state.dataset = None

# Botão para carregar dataset fictício
if st.button("Carregar dataset fictício"):
    st.session_state.dataset = criar_dataset()

# Upload do arquivo CSV
uploaded_file = st.file_uploader("Ou faça upload de um arquivo CSV com dados de crédito")
if uploaded_file:
    try:
        st.session_state.dataset = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Erro ao ler arquivo CSV: {e}")

# Se dataset estiver carregado, exibe info e permite treino
if st.session_state.dataset is not None:
    df = st.session_state.dataset
    st.write("### Dataset carregado")
    st.write(df)
    st.write(f"Dimensões: {df.shape}")
    st.write("Tipos das colunas:")
    st.write(df.dtypes)

    target = st.selectbox("Selecione a variável alvo (inadimplência):", df.columns)
    features = st.multiselect("Selecione as variáveis explicativas:", [col for col in df.columns if col != target])

    if st.button("Treinar modelo"):
        if not features:
            st.error("Por favor, selecione pelo menos uma variável explicativa.")
        else:
            try:
                X = df[features]
                y = df[target]

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

                model = LogisticRegression(max_iter=1000)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                st.subheader("Matriz de Confusão")
                st.write(confusion_matrix(y_test, y_pred))

                st.subheader("Relatório de Classificação")
                st.text(classification_report(y_test, y_pred))
            except Exception as e:
                st.error(f"Erro durante o treinamento ou avaliação do modelo: {e}")

else:
    st.info("Carregue um dataset fictício ou faça upload de um arquivo CSV para começar.")
