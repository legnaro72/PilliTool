import streamlit as st
import pandas as pd
import base64
import os
from datetime import datetime

# 1. Configurazione della Pagina
st.set_page_config(
    page_title="Email Extractor Pro - Liguria", 
    page_icon="📬", 
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

# 3. CSS Personalizzato (Arancione Istituzionale Liguria)
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
    
    # Colore Arancione Liguria (un tono circa #E85D04 o #D64D00)
    orange_liguria = "#D64D00" 
    
    st.markdown(bg_style + f"""
        <style>
        /* Pannello centrale */
        .main .block-container {{
            background-color: rgba(255, 255, 255, 0.96); 
            padding: 3rem;
            border-radius: 30px;
            box-shadow: 0 15px 45px rgba(0,0,0,0.2);
            margin-top: 2rem;
            border: 1px solid {orange_liguria};
        }}

        /* TESTI IN ARANCIONE ISTITUZIONALE LIGURIA E GRASSETTO */
        h1, h2, h3, h4, p, label, .stMarkdown, span, [data-testid="stMetricValue"] {{
            color: {orange_liguria} !important; 
            font-weight: 800 !important;
        }}

        .main-title {{
            font-size: 2.8rem !important;
            text-align: center;
            margin-bottom: 0.2rem;
        }}

        .subtitle {{ 
            text-align: center; 
            font-size: 1.2rem !important;
            margin-bottom: 2.5rem; 
            letter-spacing: 1px;
        }}
        
        /* Area Upload Stilizzata */
        [data-testid="stFileUploadDropzone"] {{
            border: 2px dashed {orange_liguria} !important;
            background-color: rgba(214, 77, 0, 0.03) !important;
            border-radius: 20px !important;
        }}

        /* Bottoni */
        .stButton>button {{
            background-color: {orange_liguria} !important;
            color: white !important;
            border-radius: 12px;
            padding: 0.8rem;
            font-weight: bold;
            width: 100%;
            border: none;
            transition: 0.3s;
        }}
        .stButton>button:hover {{
            background-color: #A33A00 !important; /* Arancione più scuro al passaggio */
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}

        /* Area Risultati */
        textarea {{
            border: 2px solid {orange_liguria} !important;
            border-radius: 10px !important;
            color: #333 !important;
            font-weight: normal !important;
        }}

        .footer {{
            text-align: center;
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 1px solid rgba(214, 77, 0, 0.2);
            color: {orange_liguria};
        }}
        </style>
    """, unsafe_allow_html=True)

apply_custom_style()

# 4. Header Logo
col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
with col_l2:
    if os.path.exists(logo_liguria_path):
        st.image(logo_liguria_path, use_column_width=True)

st.markdown("<h1 class='main-title'>📬 EMAIL EXTRACTOR PRO</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>REGIONE LIGURIA - GESTIONE CONTATTI</p>", unsafe_allow_html=True)

# GESTIONE STATO
if 'file_caricato' not in st.session_state:
    st.session_state.file_caricato = False
if 'elaborazione_conclusa' not in st.session_state:
    st.session_state.elaborazione_conclusa = False

# STEP 1: CARICAMENTO
if not st.session_state.file_caricato:
    st.markdown("### 📤 TRASCINA IL FILE EXCEL (.XLSX)")
    uploaded_file = st.file_uploader("", type="xlsx")
    if uploaded_file is not None:
        try:
            st.session_state.df = pd.read_excel(uploaded_file, engine='openpyxl')
            st.session_state.file_caricato = True
            st.rerun()
        except Exception as e:
            st.error(f"ERRORE DI CARICAMENTO: {e}")

# STEP 2: CONFIGURAZIONE
if st.session_state.file_caricato and not st.session_state.elaborazione_conclusa:
    st.markdown("### 🎯 SELEZIONA LA COLONNA DELLE EMAIL")
    colonna = st.selectbox("", st.session_state.df.columns, index=min(3, len(st.session_state.df.columns)-1))
    
    st.write("")
    if st.button("🚀 AVVIA ELABORAZIONE"):
        emails_raw = st.session_state.df[colonna].dropna().astype(str)
        seen = set()
        unique_emails = []
        log_entries = [f"--- REPORT {datetime.now().strftime('%d/%m/%Y %H:%M')} ---"]

        for idx, email in emails_raw.items():
            clean_email = email.strip().lower()
            if clean_email in seen:
                log_entries.append(f"❌ Rimosso duplicato: {clean_email}")
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
    st.markdown("### 📋 COPIA GLI INDIRIZZI (CTRL + A)")
    st.text_area(label="", value=st.session_state.risultato, height=150)
    
    m1, m2 = st.columns(2)
    m1.metric("EMAIL UNICHE", st.session_state.count_uniche)
    m2.metric("DUPLICATI ELIMINATI", st.session_state.count_duplicati)
    
    st.divider()
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button("📥 SCARICA TXT", data=st.session_state.risultato, file_name="email_pulite.txt")
    with c2:
        st.download_button("🧾 SCARICA LOG", data=st.session_state.log, file_name="log_duplicati.txt")
    with c3:
        if st.button("🔄 NUOVA ANALISI"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# Footer
st.markdown("<div class='footer'><b>REGIONE LIGURIA</b></div>", unsafe_allow_html=True)
