import streamlit as st 


def css_utils(project_name):
    # Não aparecer o sidebar
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

    # ---------------------- Simple shared CSS to match Home ----------------------
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        html, body, [class*='css'] { font-family: 'Inter', sans-serif; background-color:#f7fafc; }
        .hero-card { width:calc(100% - 120px); margin:18px 60px; padding:14px 18px; border-radius:12px;
                    background:linear-gradient(180deg, rgba(255,255,255,0.94), rgba(250,250,255,0.92));
                    box-shadow:0 10px 30px rgba(2,6,23,0.06); border:1px solid rgba(15,23,42,0.04);
                    display:flex; gap:16px; align-items:center }
        .avatar { width:52px; height:52px; border-radius:10px; background:linear-gradient(135deg,#6366f1,#3b82f6);
                display:flex; align-items:center; justify-content:center; color:white; font-weight:700; font-size:16px; }
        .hero-name { margin:0; font-size:18px; font-weight:700; color:#0f172a }
        .hero-sub { margin:4px 0 0 0; color:#475569; font-size:13px }
        .page-badge { padding:6px 10px; background:#eef2ff; color:#4338ca; border-radius:8px; font-weight:600; font-size:13px }
        .section-card { background: linear-gradient(180deg,#fff,#fbfdff); border-radius:12px; padding:14px; box-shadow:0 10px 30px rgba(2,6,23,0.04); border:1px solid rgba(15,23,42,0.04); margin:18px 60px 12px 60px; }
        .stButton>button { border-radius:10px !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(css, unsafe_allow_html=True)

    # ---------------------- Hero ----------------------
    st.markdown(
        "<div class='hero-card'>"
        "<div class='avatar'>ML</div>"
        "<div style='flex:1'>"
        f"<div class='hero-name'>{project_name}</div>"
        # "<div class='hero-sub'>Simple end-to-end demo: prepare data → train LinearRegression → forecast future prices.</div>"
        # "</div>"
            # "<div class='page-badge'>ML · Finance</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([0.2, 1, 0.2])
    with col1:
        if st.button("⬅ Voltar para Home"):
            try:
                st.switch_page("app.py")
            except Exception:
                st.experimental_set_query_params({})

css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*='css'] { font-family: 'Inter', sans-serif; background-color:#f7fafc; }

    /* Make Streamlit's main container full width (override default max-width) */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        max-width: 100% !important;
        width: 100% !important;
    }

    /* Hero / header stretches full width but keeps inner content comfortable */
    .hero-card {
        width: calc(100% - 120px);
        margin: 18px 60px; /* keep lateral breathing room */
        padding: 16px 20px;
        border-radius: 12px;
        background: linear-gradient(180deg, rgba(255,255,255,0.94), rgba(250,250,255,0.92));
        box-shadow: 0 10px 30px rgba(2,6,23,0.06);
        border: 1px solid rgba(15,23,42,0.04);
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .avatar { width:56px; height:56px; border-radius:10px;
        background: linear-gradient(135deg,#6366f1,#3b82f6);
        display:flex; align-items:center; justify-content:center; color:white; font-weight:700; font-size:18px;
        box-shadow: 0 6px 18px rgba(59,130,246,0.10); }

    .hero-name { margin:0; font-size:20px; font-weight:700; color:#0f172a; display:block; }
    .hero-sub { margin:4px 0 0 0; color:#475569; font-size:13px; }
    .page-badge { padding:6px 10px; background:#eef2ff; color:#4338ca; border-radius:8px; font-weight:600; font-size:13px; }

    /* Cards area: allow stretching, but center content and limit per-row spacing */
    .cards-wrap {
        width: calc(100% - 120px);
        margin: 18px 60px;
        display: block;
    }

    .section-card {
        background: linear-gradient(180deg,#fff,#fbfdff);
        border-radius:12px;
        padding:14px;
        box-shadow:0 10px 30px rgba(2,6,23,0.04);
        border:1px solid rgba(15,23,42,0.04);
        margin-bottom:18px;
        width: calc(100% - 40px);
    }

    .card {
        background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
        border-radius: 14px;
        box-shadow: 0 8px 30px rgba(2,6,23,0.05);
        overflow: hidden;
        transition: all 0.28s cubic-bezier(.2,.9,.2,1);
        border: 1px solid rgba(15,23,42,0.05);
        position: relative;
        margin-bottom: 12px;
    }

    .card img { width:100%; height:160px; object-fit:cover; display:block }
    .card-content { padding:16px }
    .card-title { font-size:17px; font-weight:700; color:#0f172a; margin-bottom:6px }
    .card-subtitle { font-size:13px; color:#6b7280; margin-bottom:8px }
    .card-text { font-size:13px; color:#374151; margin-bottom:12px; line-height:1.4 }

    .kpis { display:flex; gap:18px; align-items:center; width:100%; }
    .metric-label { color:#6b7280; font-size:13px; margin-bottom:6px; }
    .metric-value { font-weight:700; font-size:18px; color:#0f172a; }

    /* Streamlit native button styling (keeps look consistent) */
    .stButton>button { width:100%; padding:10px 14px; border-radius:10px !important;
        background: linear-gradient(90deg,#4f46e5,#3b82f6) !important; color:#fff !important; font-weight:700 !important;
        border:none !important; box-shadow: 0 8px 22px rgba(59,130,246,0.12) !important; }

    /* Chart container stretch */
    .stAltairChart, .stChart { width: 100% !important; }

    @media (max-width: 900px){
        .hero-card, .cards-wrap { margin-left: 18px; margin-right: 18px; width: calc(100% - 36px); }
        .section-card { width: calc(100% - 36px); }
    }
    </style>
    """