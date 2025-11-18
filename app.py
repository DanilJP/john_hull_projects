import streamlit as st
from utils.projects import projects

st.set_page_config(page_title="Portfólio — Daniel Juliano", layout="wide",initial_sidebar_state="collapsed")
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        /* Ajusta conteúdo para ocupar largura total */
        [data-testid="stSidebarNav"] { 
            display: none;
        }
        [data-testid="main-menu"] {
            visibility: hidden;
        }
        [data-testid="collapsedControl"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)
# ---------------------- CSS + animação ----------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*='css']  {font-family: 'Inter', sans-serif; background-color:#f7fafc;}

    /* header / hero */
    .hero-card { max-width: 960px; margin: 28px auto 12px auto; padding: 18px 22px; border-radius: 14px;
        background: linear-gradient(180deg, rgba(255,255,255,0.85), rgba(250,250,255,0.7));
        box-shadow: 0 8px 30px rgba(15,23,42,0.06); border: 1px solid rgba(15,23,42,0.04);
        display: flex; align-items: center; gap: 18px; }

    .avatar { width: 64px; height: 64px; border-radius: 12px;
        background: linear-gradient(135deg, #6366f1, #3b82f6);
        display:flex; align-items:center; justify-content:center; color:white; font-weight:700; font-size:20px;
        box-shadow: 0 6px 18px rgba(59,130,246,0.12); }

    .hero-text { flex:1 }
    .hero-name { margin: 0; font-size:28px; font-weight:700; line-height:1;
        background: linear-gradient(90deg,#0f172a,#111827); -webkit-background-clip: text; color: transparent; display:inline-block; }

    .hero-sub { margin: 4px 0 0 0; color:#475569; font-size:14px; }
    .hero-badge { padding:8px 12px; background:#eef2ff; color:#4338ca; border-radius:10px; font-weight:600; font-size:13px; }

    /* cards area */
    .cards-wrap { max-width: 1200px; margin: 18px auto; display:block; }
    .card { background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%); border-radius: 14px;
        box-shadow: 0 8px 30px rgba(2,6,23,0.05); overflow: hidden; transition: all 0.28s cubic-bezier(.2,.9,.2,1);
        border: 1px solid rgba(15,23,42,0.05); position: relative; margin-bottom: 12px; }

    .card:hover { transform: translateY(-8px); box-shadow: 0 22px 45px rgba(2,6,23,0.09); border-color: rgba(59,130,246,0.12); }
    .card::before { content: ""; position: absolute; top:0; left:0; right:0; height:4px; background: linear-gradient(90deg, #6366f1, #3b82f6, #06b6d4); opacity:0; transition:opacity .25s ease; }
    .card:hover::before { opacity:1 }
    .card img { width:100%; height:160px; object-fit:cover; display:block }
    .card-content { padding:16px }
    .card-title { font-size:17px; font-weight:700; color:#0f172a; margin-bottom:6px }
    .card-subtitle { font-size:13px; color:#6b7280; margin-bottom:8px }
    .card-text { font-size:13px; color:#374151; margin-bottom:12px; line-height:1.4 }
    .tag { display:inline-block; background:#eef2ff; border-radius:999px; padding:6px 10px; font-size:12px; margin:3px 6px 0 0; color:#4338ca; font-weight:600 }

    .card-footer { padding: 0 16px 16px 16px; }

    /* botão nativo st.button estilizado */
    .stButton>button {
        width: 100%;
        padding: 10px 14px;
        border-radius: 12px !important;
        background: linear-gradient(90deg, #4f46e5, #3b82f6) !important;
        color: #fff !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 8px 22px rgba(59,130,246,0.12) !important;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 14px 34px rgba(59,130,246,0.18) !important; }

    /* animação fade + slide pra cima */
    @keyframes fadeUp {
      0% { opacity: 0; transform: translateY(18px); }
      100% { opacity: 1; transform: translateY(0); }
    }

    /* garante que cada card comece invisível - o inline style define delay e animação */
    .card[data-animate="true"] {
      /* animation and delay are applied inline to allow stagger */
    }

    @media (max-width: 640px) {
      .hero-card { padding: 12px; gap:12px }
      .hero-name { font-size:20px }
      .cards-wrap { padding: 0 12px }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------- Header / Hero ----------------------
st.markdown(
    "<div class='hero-card'>"
    "<div class='avatar'>DJ</div>"
    "<div class='hero-text'>"
    "<div class='hero-name'>Daniel Juliano</div>"
    "<div class='hero-sub'>Projetos selecionados em dados, finanças e automações — clique em um card para ver mais.</div>"
    "</div>"
    "<div class='hero-badge'>Analista Quant</div>"
    "</div>",
    unsafe_allow_html=True,
)

# ---------------------- Cards (com stagger animation) ----------------------
st.markdown("<div class='cards-wrap'>", unsafe_allow_html=True)

cols_per_row = 3
rows = [projects[i:i+cols_per_row] for i in range(0, len(projects), cols_per_row)]

# contador global para calcular delay
global_index = 0
for row in rows:
    cols = st.columns(len(row))
    for col, proj in zip(cols, row):
        with col:
            # delay stagger (em segundos). 0.06-0.12 é um bom intervalo visual
            delay = round(global_index * 0.08, 2)
            # inline style aplica delay e animação; data-animate para futura manipulação se quiser
            style = f"opacity:0; animation: fadeUp .48s cubic-bezier(.2,.9,.2,1) forwards; animation-delay: {delay}s;"
            st.markdown(f"""
            <div class='card' data-animate="true" style="{style}">
                <img src="{proj['image']}" alt="{proj['title']}"/>
                <div class='card-content'>
                    <div class='card-title'>{proj['title']}</div>
                    <div class='card-subtitle'>{proj['subtitle']}</div>
                    <div class='card-text'>{proj['short']}</div>
                    {''.join([f"<span class='tag'>{t}</span>" for t in proj['tags']])}
                </div>
            </div>
            """, unsafe_allow_html=True)

            global_index += 1

            # botão fora do card (nativo) - aparece abaixo de cada card
            if st.button("Ver projeto →", key=f"btn_{proj['id']}"):
                # usa API do Streamlit para trocar de página. Ajuste se sua versão não suportar.
                st.switch_page("pages/"+proj['file'])
                # except Exception:
                #     # fallback: navegação via query params (mantém dentro da mesma página)
                #     st.experimental_set_query_params(proj=proj['id'])

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------- Footer ----------------------
# st.markdown("---")
# st.markdown("**Como adicionar novos projetos:** adicione um dicionário em `projects` com: `id`, `file`, `title`, `subtitle`, `short`, `image`, `tags`.")
