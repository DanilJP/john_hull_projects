import streamlit as st
import numpy as np

st.set_page_config(page_title="Taxa Zero", layout="centered")

st.markdown("<h1 style='text-align: left;'>🎯 Taxa Zero (ou Taxa à Vista)</h1>", unsafe_allow_html=True)

# Resumo explicativo
st.markdown("""
A **taxa de juros zero** de `n` anos é a taxa obtida em um investimento que:
- Começa hoje
- **Não tem pagamentos intermediários**
- Paga **juros e principal somente no final**

Também chamada de:
- **Taxa à vista**
- **Zero de n anos**

---

### 📘 Exemplo:

Se a taxa zero de 5 anos for **5% ao ano com capitalização contínua**, então $100 investidos hoje crescem até:

```math
100 * e^(0.05 * 5) = $128,40""")
