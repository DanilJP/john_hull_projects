import streamlit as st

st.set_page_config(page_title="📈 Termo vs Futuro", layout="centered")
st.title("📈 Diferença entre Preço a Termo e Preço Futuro")

st.markdown("""
### 📚 Contexto
Embora frequentemente tratemos os preços **a termo (forward)** e **futuros** como iguais, isso só é exato quando:

- A **taxa de juros livre de risco é constante**;
- Ou seu comportamento futuro é **totalmente previsível**.

---

### 🧠 Quando **são diferentes**?

Se a taxa de juros varia aleatoriamente, como no mundo real, e o **preço do ativo** está **correlacionado com as taxas de juros**, então:

- **Futuros comprados** se beneficiam de ajustes diários que são **reinvestidos a taxas maiores** (quando S ↑ e juros ↑).
- Ou sofrem **perdas menores** por serem financiadas a taxas menores (quando S ↓ e juros ↓).

Isso faz com que os **futuros tendam a ser ligeiramente maiores que os termos** quando há correlação positiva entre preço do ativo e taxa de juros.

---

### 📊 Comparativo

| Característica              | Contrato a Termo     | Contrato Futuro         |
|-----------------------------|----------------------|--------------------------|
| Ajuste Diário               | ❌ Não                | ✅ Sim                   |
| Liquidez                    | Média                | Alta                    |
| Garantia / Risco de Crédito| Bilateral            | Câmara de Compensação   |
| Impacto da Volatilidade da Taxa de Juros | Menor           | Maior (via ajustes)     |

---

### 📌 Conclusão

> Em **modelos teóricos simplificados**, consideramos Futuros ≈ Termos  
> Na prática, a diferença existe — mas é pequena e muitas vezes desprezível  
> (exceto casos específicos como **futuros de eurodólares** — ver seção 6.3).
""")
