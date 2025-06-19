import streamlit as st

st.set_page_config(page_title="📘 Premissas e Notação - Hull", layout="centered")
st.title("📘 Premissas e Notação")

st.markdown("## 📌 Premissas do Modelo")
st.markdown("""
Os modelos de precificação de contratos a termo e futuros se baseiam em algumas **premissas teóricas ideais**:

1. **Sem custos de transação** ao negociar ativos.
2. Todos os agentes estão sujeitos à **mesma alíquota de imposto** sobre lucros líquidos.
3. Participantes podem **emprestar e tomar emprestado à mesma taxa de juros livre de risco**.
4. **Oportunidades de arbitragem são imediatamente exploradas** pelos principais agentes de mercado.

> Essas premissas não precisam ser verdadeiras para todos os participantes, mas sim para os principais, como grandes bancos e fundos.
""")

st.markdown("## 🔢 Notação Padrão")
st.table({
    "Símbolo": ["T", "S₀", "F₀", "r"],
    "Significado": [
        "Tempo até a entrega (em anos)",
        "Preço à vista atual do ativo",
        "Preço a termo/futuro hoje",
        "Taxa livre de risco (com capitalização contínua)"
    ]
})

st.markdown("---")
st.caption("Essas premissas e notações serão a base dos cálculos de arbitragem e precificação nos próximos tópicos.")
