import streamlit as st
import pandas as pd

st.set_page_config(page_title="📉 Teorias da Estrutura a Termo das Taxas de Juros")

st.title("Teorias da Estrutura a Termo das Taxas de Juros")

st.markdown("""
Nesta página, abordamos as principais teorias que explicam o formato da curva à vista das taxas de juros:

- **Teoria das Expectativas:** As taxas longas refletem as taxas de curto prazo futuras esperadas.
- **Teoria da Segmentação do Mercado:** Cada segmento (curto, médio, longo prazo) é determinado pela oferta e demanda específica, sem relação direta entre eles.
- **Teoria da Preferência pela Liquidez:** Investidores preferem liquidez, levando a taxas longas mais altas para compensar o risco e menor liquidez.
""")

# Mostrar tabelas do exemplo do banco

st.header("Exemplo: Taxas de Depósito e Hipoteca de um Banco")

st.write("Taxas da tabela 4.7:")

tabela_4_7 = {
    "Vencimento (anos)": [1, 5],
    "Taxa de Depósito (%)": [3, 3],
    "Taxa de Hipoteca (%)": [6, 6]
}
df_4_7 = pd.DataFrame(tabela_4_7)
st.table(df_4_7)

st.write("""
Na situação acima, a maioria dos depositantes escolhe depósitos de 1 ano e a maioria dos tomadores escolhe hipotecas de 5 anos, criando desequilíbrio e risco para o banco.
""")

st.write("Taxas da tabela 4.8 (ajuste para reduzir desequilíbrio):")

tabela_4_8 = {
    "Vencimento (anos)": [1, 5],
    "Taxa de Depósito (%)": [3, 4],
    "Taxa de Hipoteca (%)": [6, 7]
}
df_4_8 = pd.DataFrame(tabela_4_8)
st.table(df_4_8)

st.write("""
Com essas taxas ajustadas, os depositantes tendem a migrar para depósitos de 5 anos e os tomadores para hipotecas de 1 ano, melhorando o alinhamento dos ativos e passivos do banco.
""")

# Simulação interativa

st.header("Simulação de escolha dos clientes")

deposito_1a = st.slider("Porcentagem de depositantes que escolhem depósito de 1 ano (%)", 0, 100, 70)
deposito_5a = 100 - deposito_1a
hipoteca_1a = st.slider("Porcentagem de tomadores que escolhem hipoteca de 1 ano (%)", 0, 100, 30)
hipoteca_5a = 100 - hipoteca_1a

st.markdown("---")

st.write(f"Depositantes: {deposito_1a}% escolhem 1 ano, {deposito_5a}% escolhem 5 anos.")
st.write(f"Tomadores: {hipoteca_1a}% escolhem 1 ano, {hipoteca_5a}% escolhem 5 anos.")

# Exemplo simples do impacto para o banco

st.header("Estimativa simples de risco de liquidez e renda líquida")

taxa_deposito_1a = 0.03
taxa_deposito_5a = 0.04
taxa_hipoteca_1a = 0.06
taxa_hipoteca_5a = 0.07

# Calculando custo médio dos depósitos
custo_depositos = (deposito_1a / 100) * taxa_deposito_1a + (deposito_5a / 100) * taxa_deposito_5a
# Receita média das hipotecas
receita_hipotecas = (hipoteca_1a / 100) * taxa_hipoteca_1a + (hipoteca_5a / 100) * taxa_hipoteca_5a

renda_liquida = receita_hipotecas - custo_depositos

st.write(f"Custo médio ponderado dos depósitos: {custo_depositos*100:.2f}%")
st.write(f"Receita média ponderada das hipotecas: {receita_hipotecas*100:.2f}%")
st.write(f"**Renda líquida de juros estimada:** {renda_liquida*100:.2f}%")

st.markdown("""
> Quanto maior a renda líquida, melhor para a estabilidade financeira do banco. Desequilíbrios nos vencimentos dos ativos e passivos podem reduzir essa renda e aumentar o risco do banco.
""")

st.markdown("#### Dica: Ajuste as escolhas dos clientes e veja como a renda líquida muda.")

