import streamlit as st
import pandas as pd
import numpy as np

# Configuração visual
st.set_page_config(page_title="Projetos Quant")
st.markdown("<h1 style='text-align: left;'>💼 Estimativas de probabilidades de inadimplência a partir de rendimentos de títulos</h1>", unsafe_allow_html=True)

spreads = {
    "Tempo (anos)" : [1,2,3],
    "Spreads" : [150,180,195],
    "Rendimentos" : [0.065,0.068,0.0695]
}

spreads = pd.DataFrame(data=spreads)
st.dataframe(spreads,hide_index=True)

def cal_risco_medio(t,R):
    try:
        spread = spreads[spreads['Tempo (anos)'] == t]['Spreads'].iloc[0]
        spread = spread/100
        R_perc = R / 100
        risco_medio = spread / (1 - R_perc)
        return risco_medio
    except:
        risco_medio = 0
        return risco_medio

# Mostrar tabela
st.write('Utilizando a tabela acima, podemos calcular : ')

st.markdown("#### 📊 Exemplo, estimativa até o fim do período selecionado :")
col1, col2 = st.columns(2)
tempo_escolhido = col1.number_input("Até o tempo (ano)", min_value=1, step=1, max_value=3, value=1)
rec_estimada = col2.number_input("Recuparação estimada (%)", min_value=1, step=1, max_value=100, value=40)
risco_medio = cal_risco_medio(tempo_escolhido,rec_estimada)
st.success(f"Taxa de risco médio (λ): **{risco_medio:.2f}%**")

st.write('_________________________________________________________')
st.markdown("#### 📊 Exemplo, estimativa durante o ano selecionado :")

col3, col4 = st.columns(2)
tempo_escolhido = col3.number_input("Durante o tempo (ano)", min_value=1, step=1, max_value=3, value=1,key=1)
rec_estimada = col4.number_input("Recuparação estimada (%)", min_value=1, step=1, max_value=100, value=40,key=2)
risco_medio_entre = (tempo_escolhido * cal_risco_medio(tempo_escolhido,rec_estimada)) - ((tempo_escolhido-1)*cal_risco_medio(tempo_escolhido-1,rec_estimada))
try:
    st.success(f"Taxa de risco médio (λ) durante o ano {tempo_escolhido} : **{risco_medio_entre:.2f}%**")
except:
    st.success(f"Taxa de risco médio (λ) durante o ano {tempo_escolhido} : **3,00%**")

st.write('_________________________________________________________')
st.markdown("#### 📊 Correspondência de preços de títulos :")

col5, col6, col7, col8 = st.columns(4)
tempo_escolhido = col5.number_input("Durante o tempo (ano)", min_value=1, step=1, max_value=3, value=1,key=5)
taxa_livre_risco = col6.number_input("Taxa livre de risco (%):", min_value=1, step=1, max_value=100, value=5,key=6)
valor_cupom = col7.number_input("Cupom semestral ($):", min_value=1, step=1, max_value=100, value=4,key=7)
rec_estimada = col8.number_input("Recuparação estimada (%)", min_value=1, step=1, max_value=100, value=40,key=8)

rendimento = spreads[spreads['Tempo (anos)'] == tempo_escolhido]['Rendimentos'].iloc[0]

# Valor do título a partir dos rendimentos
def calcula_valor(face,desconto,tempo,cupom):
    valor_final = 0
    sem = 0.5
    while sem <= tempo:
        if sem == tempo:
            valor = cupom + face
            valor = valor * np.exp(-sem*desconto)
        else:
            valor = cupom * np.exp(-sem*desconto)
        valor_final = valor_final + valor
        sem = sem + 0.5
    return round(valor_final,2)

valor_rendimento = calcula_valor(100,rendimento,tempo_escolhido,valor_cupom)
st.info(f'Valor do título a partir do rendimento : ${valor_rendimento}')
valor_taxa_livre = calcula_valor(100,taxa_livre_risco/100,tempo_escolhido,valor_cupom)
st.info(f'Valor do título a partir da taxa livre de risco : ${valor_taxa_livre}')
diff_valor_inadimplencia = round(valor_taxa_livre - valor_rendimento,2)
st.info(f'Valor presente da perda esperada : ${diff_valor_inadimplencia}')

def calcula_valor_tempo_medio(face,desconto,tempo,cupom,sem):
    valor_final = 0
    while sem <= tempo-0.25:
        if sem == tempo-0.25:
            valor = cupom + face
            valor = valor * np.exp(-sem*desconto)
        else:
            valor = cupom * np.exp(-sem*desconto)
        valor_final = valor_final + valor
        sem = sem + 0.5
    return round(valor_final,2)

sem = 0.25
while sem <= tempo_escolhido-0.25:
    valor_tempo_medio = calcula_valor_tempo_medio(100,taxa_livre_risco/100,tempo_escolhido,valor_cupom,sem)
    st.info(f'Valor do título a partir da taxa livre de risco no tempo médio {int(sem*12)} meses : ${valor_tempo_medio}')
    sem = sem + 0.5
    