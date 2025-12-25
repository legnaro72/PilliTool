import streamlit as st
import pandas as pd
import base64
import os
from datetime import datetime

# 1. Configurazione della Pagina
st.set_page_config(
    page_title="Email Extractor Pro - Liguria", 
    page_icon="📧", 
    layout="centered"
)

# 2. Funzione per codificare lo sfondo in Base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

img_bg_base64 = get_base64_image("no.png")
logo_liguria_path = "Logo Liguria.png"

# 3. CSS Personalizzato (Verde Istituzionale + Box Istruzioni)
def apply_custom_style():
    bg_style = ""
    if img_bg_base64:
        bg_style = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{img_bg_base64}");
            background-attachment: fixed;
            background-size: cover;
            background-position: center;
        }}
        </style>
        """
    
    orange_liguria = "#D64D00"
    green_liguria = "#166534"
    
    st.markdown(bg_style + f"""
        <style>
        /* Contenitore principale */
        .main .block-container {{
            background-color: rgba(255, 255, 255, 0.97); 
            padding: 3rem;
            border-radius: 25px;
            box-shadow: 0 15px 50px rgba(0,0,0,0.2);
            margin-top: 2rem;
        }}

        /* EFFETTO TASTO PER LE SCRITTE (BADGE) */
        .instruction-box {{
            background-color: #FFF5F0;
            border: 2px solid {orange_liguria};
            padding: 10px 20px;
            border-radius: 10px;
            color: {orange_liguria};
            font-weight: 800;
            display: inline-block;
            margin-bottom: 15px;
            text-transform: uppercase;
            font-size: 0.9rem;
        }}

        h1 {{ 
            color: {green_liguria} !important; 
            font-weight: 900 !important; 
            text-align: center;
        }}

        /* BOTTONI VERDI (ISTITUZIONALI) */
        .stButton>button, .stDownloadButton>button {{
            background-color: {green_liguria} !important;
            color: white !important;
            border-radius: 8px;
            padding: 0.7rem;
            font-weight: bold;
            width: 100%;
            border: none;
            transition: 0.3s;
        }}
        .stButton>button:hover, .stDownloadButton>button:hover {{
            background-color: #0d3d1f !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}

        /* Area Risultati */
        textarea {{
            border: 2px solid {green_liguria} !important;
            border-radius: 10px !important;
            font-family: 'Consolas', monospace !important;
        }}

        /* Footer */
        .footer {{
            text-align: center;
            margin-top: 3rem;
            color: {green_liguria};
            font-weight: bold;
        }}
        </style>
    """, unsafe_allow_html=True)

apply_custom_style()

# 4. Header Logo
col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
with col_l2:
    if os.path.exists(logo_liguria_path):
        st.image(logo_liguria_path, use_column_width=True)

st.markdown("<h1>📬 EMAIL EXTRACTOR PRO</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:{green_liguria}; font-weight:bold;'>REGIONE LIGURIA</p>", unsafe_allow_html=True)

# GESTIONE STATO
if 'file_caricato' not in st.session_state:
    st.session_state.file_caricato = False
if 'elaborazione_conclusa' not in st.session_state:
    st.session_state.elaborazione_conclusa = False

# STEP 1: CARICAMENTO
if not st.session_state.file_caricato:
    st.markdown('<div class="instruction-box">📂 CARICAMENTO: TRASCINA IL FILE EXCEL</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type="xlsx")
    if uploaded_file is not None:
        try:
            st.session_state.df = pd.read_excel(uploaded_file, engine='openpyxl')
            st.session_state.file_caricato = True
            st.rerun()
        except Exception as e:
            st.error(f"Errore: {e}")

# STEP 2: CONFIGURAZIONE
if st.session_state.file_caricato and not st.session_state.elaborazione_conclusa:
    st.markdown('<div class="instruction-box">🎯 CONFIGURAZIONE: SCEGLI LA COLONNA</div>', unsafe_allow_html=True)
    colonna = st.selectbox("", st.session_state.df.columns, index=min(3, len(st.session_state.df.columns)-1))
    
    st.write("")
    if st.button("🚀 GENERA LISTA EMAIL"):
        emails_raw = st.session_state.df[colonna].dropna().astype(str)
        seen = set()
        unique_emails = []
        log_entries = [f"REPORT {datetime.now().strftime('%H:%M')}"]

        for idx, email in emails_raw.items():
            clean_email = email.strip().lower()
            if clean_email in seen:
                log_entries.append(f"DUPLICATO: {clean_email}")
            else:
                seen.add(clean_email)
                unique_emails.append(clean_email)
        
        unique_emails.sort(key=lambda x: (x.split("@")[1] if "@" in x else "", x))
        
        st.session_state.risultato = ", ".join(unique_emails)
        st.session_state.log = "\n".join(log_entries)
        st.session_state.count_uniche = len(unique_emails)
        st.session_state.count_duplicati = len(log_entries)-1
        st.session_state.elaborazione_conclusa = True
        st.rerun()

# STEP 3: RISULTATO FINALE
if st.session_state.elaborazione_conclusa:
    st.markdown('<div class="instruction-box">📋 RISULTATO: SELEZIONA E COPIA (CTRL + A)</div>', unsafe_allow_html=True)
    st.text_area(label="", value=st.session_state.risultato, height=150)
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown(f"<div style='color:{green_liguria}; font-weight:900;'>EMAIL UNICHE: {st.session_state.count_uniche}</div>", unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"<div style='color:{orange_liguria}; font-weight:900;'>DUPLICATI RIMOSSI: {st.session_state.count_duplicati}</div>", unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown('<div class="instruction-box">📥 DOWNLOAD DOCUMENTI</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button("SCARICA TXT", data=st.session_state.risultato, file_name="email_pulite.txt")
    with c2:
        st.download_button("SCARICA LOG", data=st.session_state.log, file_name="log_duplicati.txt")
    with c3:
        if st.button("🔄 RE-START"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# Footer
st.markdown("<div class='footer'>REGIONE LIGURIA</div>", unsafe_allow_html=True)
