import streamlit as st
import numpy as np
from scipy.optimize import brentq

st.set_page_config(page_title="Determinação das Taxas Zero", layout="centered")

st.markdown("<h1 style='text-align: left;'>🧮 Determinação das Taxas Zero do Tesouro (Bootstrap)</h1>", unsafe_allow_html=True)

st.markdown("""
A curva de taxas zero pode ser obtida usando o **método bootstrap** a partir dos preços de títulos do Tesouro.

- Títulos **zero cupom** (strips) permitem cálculo direto das taxas zero.
- Para títulos com cupons, usa-se as taxas zero já conhecidas para descontar os cupons anteriores e calcular a taxa zero para o último pagamento.

---

### Exemplo simplificado:

| Vencimento (anos) | Cupom anual (%) | Preço do título ($) |
|-------------------|-----------------|---------------------|
| 0.25              | 0               | 97,5                |
| 0.50              | 0               | 94,9                |
| 1.00              | 0               | 90,0                |
| 1.50              | 8               | 96,0                |
| 2.00              | 12              | 101,6               |

Para o título de 0,25 ano (zero cupom), a taxa zero R satisfaz:
$$
100 = 97,5 \t e^{R \t 0,25}
$$

E para títulos com cupons, por exemplo o de 1,5 ano:
$$
96 = 4e^{-R_{0,5} \t 0,5} + 4e^{-R_{1,0} \t 1,0} + 104e^{-R_{1,5} \t 1,5}
$$

Usando as taxas zero previamente calculadas para 0,5 e 1,0 ano, podemos resolver para \(R_{1,5}\).

---

A curva de taxas zero resultante é conhecida como **curva à vista (zero curve)**.
""")

st.divider()

# Função para calcular taxa zero para título zero cupom
def taxa_zero_zero_cupom(preco, principal, tempo):
    return -np.log(preco/principal) / tempo

# Função para calcular taxa zero para títulos com cupom via bootstrap
def taxa_zero_bootstrap(precos, cupons, tempos, principal):
    taxas = []
    for i in range(len(cupons)):
        if cupons[i] == 0:
            R = taxa_zero_zero_cupom(precos[i], principal, tempos[i])
            taxas.append(R)
        else:
            # Resolve para a taxa zero do último fluxo descontado
            def f(R):
                soma = 0
                for j in range(i):
                    soma += (cupons[i]/2) * np.exp(-taxas[j] * tempos[j])
                soma += (cupons[i]/2 + principal) * np.exp(-R * tempos[i])
                return precos[i] - soma
            R_sol = brentq(f, 0, 1)
            taxas.append(R_sol)
    return taxas

# Dados do exemplo
principal = 100
vencimentos = [0.25, 0.50, 1.00, 1.50, 2.00]
cupons_anuais = [0, 0, 0, 8, 12]
precos_titulos = [97.5, 94.9, 90.0, 96.0, 101.6]

if st.button("Calcular taxas zero via bootstrap"):
    taxas_zero = taxa_zero_bootstrap(precos_titulos, cupons_anuais, vencimentos, principal)
    st.markdown("### 🧾 Taxas zero calculadas (com capitalização contínua)")
    for v, r in zip(vencimentos, taxas_zero):
        st.write(f"{v:.2f} anos: {r*100:.3f}% ao ano")
else:
    st.info("Clique no botão para calcular as taxas zero.")
