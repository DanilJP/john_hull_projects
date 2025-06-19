import streamlit as st

st.set_page_config(page_title="📉 Venda a Descoberto - Hull", layout="centered")
st.title("📉 Simulador de Venda a Descoberto (Short Selling)")

st.markdown("""
Venda a descoberto é uma estratégia onde o investidor vende ações que ele **não possui**, esperando que o preço caia para recomprá-las mais barato.

Nesta calculadora, vamos estimar o lucro ou prejuízo da operação, considerando dividendos pagos durante o período e valores de venda/recompra.
""")

st.header("🔢 Parâmetros da Operação")

col1, col2 = st.columns(2)
with col1:
    preco_venda = st.number_input("💰 Preço de venda inicial por ação", value=120.0)
    dividendos = st.number_input("💵 Dividendos pagos por ação durante o período", value=1.0)
with col2:
    preco_recompra = st.number_input("📈 Preço de recompra por ação", value=100.0)
    quantidade = st.number_input("📊 Quantidade de ações", value=500, step=100)

lucro_bruto = quantidade * (preco_venda - preco_recompra)
custo_dividendos = quantidade * dividendos
lucro_liquido = lucro_bruto - custo_dividendos

st.markdown("---")
st.subheader("📊 Resultado da Operação")

st.write(f"🔹 Lucro bruto (sem dividendos): **R$ {lucro_bruto:,.2f}**")
st.write(f"🔸 Custo com dividendos: **R$ {custo_dividendos:,.2f}**")
st.success(f"✅ Lucro líquido: **R$ {lucro_liquido:,.2f}**")

st.markdown("---")
st.caption("Cenário baseado no exemplo do livro de Hull (Cap. 5).")
