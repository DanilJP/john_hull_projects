import streamlit as st
import numpy as np

st.set_page_config(page_title="Apreçamento de Títulos", layout="centered")

# Título
st.markdown("<h1 style='text-align: left;'>📊 Apreçamento de Títulos</h1>", unsafe_allow_html=True)

# Resumo teórico
st.markdown("""
A maioria dos títulos paga **cupons periódicos** e o **principal no vencimento**.  
O **preço teórico** de um título é o **valor presente de todos os fluxos de caixa futuros**, descontados por taxas zero específicas para cada período.

---

### 🎯 Conceitos principais:

- **Taxa zero**: taxa para descontar cada fluxo com capitalização contínua.
- **Rendimento do título (Yield)**: taxa única que ajusta o preço presente ao preço de mercado.
- **Rendimento par**: taxa de cupom que faz o preço do título ser igual ao valor de face.

---

📘 *Exemplo* para um título de 2 anos com cupons semestrais de 6% e taxas zero compostas continuamente:

| Vencimento | Taxa Zero |
|------------|-----------|
| 0.5 ano    | 5.0%      |
| 1.0 ano    | 5.8%      |
| 1.5 ano    | 6.4%      |
| 2.0 anos   | 6.8%      |

Preço teórico calculado como:  
3 * e^(-0.05 * 0.5) + 3 * e^(-0.058 * 1) + 3 * e^(-0.064 * 1.5) + 103 * e^(-0.068 * 2) = 98,39
""")

st.divider()

# Calculadora de preço teórico
st.markdown("### 💸 Calculadora de Preço de Título com Cupons")

valor_face = st.number_input("🔢 Valor de face do título ($)", value=100.0)
taxa_cupom_ano = st.number_input("💰 Taxa do cupom (% ao ano)", value=6.0)
frequencia = st.selectbox("📆 Frequência dos cupons (por ano)", [1, 2, 4], index=1)  # semestral padrão
n_anos = st.number_input("📈 Tempo até o vencimento (anos)", value=2.0)
taxas_zero_input = st.text_area(
    "📉 Informe as taxas zero por período (%, separadas por vírgula):",
    value="5.0, 5.8, 6.4, 6.8"
)

# Processa taxas zero
try:
    taxas_zero = [float(t.strip()) / 100 for t in taxas_zero_input.split(",")]
except:
    st.error("Erro ao processar as taxas zero. Use vírgula para separar e números válidos.")
    st.stop()

n_pagamentos = int(n_anos * frequencia)
cupom = valor_face * (taxa_cupom_ano / 100) / frequencia
periodos = [(i + 1) / frequencia for i in range(n_pagamentos)]

if len(taxas_zero) < n_pagamentos:
    st.warning(f"⚠️ Informe ao menos {n_pagamentos} taxas zero (uma para cada período).")
else:
    preco = 0
    for i in range(n_pagamentos):
        fluxo = cupom if i < n_pagamentos - 1 else cupom + valor_face
        desconto = np.exp(-taxas_zero[i] * periodos[i])
        preco += fluxo * desconto

    st.success(f"💲 Preço teórico do título: R$ {preco:.2f}")
