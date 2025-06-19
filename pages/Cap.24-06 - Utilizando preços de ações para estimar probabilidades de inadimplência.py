import streamlit as st
import pandas as pd
import numpy as np
from scipy.optimize import root_scalar

# Configuração visual
st.set_page_config(page_title="Projetos Quant")
st.markdown("<h1 style='text-align: left;'>💼 Utilizando preços de ações para estimar probabilidades de inadimplência</h1>", unsafe_allow_html=True)
