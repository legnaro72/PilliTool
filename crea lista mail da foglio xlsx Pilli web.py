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

# 2. Funzione per codificare le immagini in Base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

img_bg_base64 = get_base64_image("no.png")
logo_liguria_path = "Logo Liguria.png"
pilly_ico_path = "pilly.ico" # Assicurati che 'pilly.ico' sia nella stessa directory

# 3. CSS Personalizzato (Colori e Logica Modificati)
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
    
    # Colori richiesti
    orange_req = "rgb(255, 165, 0)"
    green_liguria = "#1E8449" 
    
    st.markdown(bg_style + f"""
        <style>
        /* Pannello centrale */
        .main .block-container {{
            background-color: rgba(255, 255, 255, 0.98); 
            padding: 3rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-top: 2rem;
        }}

        /* TITOLO PRINCIPALE E SOTTOTITOLO ARANCIONE */
        .main-title, .app-subtitle {{
            color: {orange_req} !important;
            font-weight: 900 !important;
            text-align: center;
            margin-bottom: 0.5rem;
        }}
        .main-title {{ font-size: 3rem !important; }}
        .app-subtitle {{ font-size: 1.2rem; }}

        /* BADGE ISTRUZIONI (Sfondo Verde, Testo Arancione) */
        .instruction-badge {{
            background-color: {green_liguria} !important;
            border: 2px solid {orange_req};
            padding: 12px 20px;
            border-radius: 10px;
            color: {orange_req} !important; /* Testo arancione */
            font-weight: 900;
            margin-bottom: 20px;
            text-transform: uppercase;
            display: block;
            text-align: center;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        }}

        /* TASTI (VERDI CON SCRITTA BIANCA) */
        div.stButton > button, .stDownloadButton > button {{
            background-color: {green_liguria} !important;
            color: white !important;
            border-radius: 8px;
            padding: 0.8rem;
            font-weight: bold !important;
            font-size: 1.1rem !important;
            width: 100%;
            border: 1px solid {orange_req};
        }}
        
        /* Area Risultati */
        textarea {{
            border: 2px solid {green_liguria} !important;
            border-radius: 10px !important;
            font-family: 'Consolas', monospace !important;
        }}

        /* Metriche (Scritte Arancioni) */
        [data-testid="stMetricValue"] {{
            color: {orange_req} !important; /* Valori metriche arancioni */
            font-weight: 900 !important;
        }}
        [data-testid="stMetricLabel"] {{
            color: {orange_req} !important; /* Etichette metriche arancioni */
            font-weight: 900 !important;
        }}

        .footer {{
            text-align: center;
            margin-top: 3rem;
            color: {orange_req}; /* Footer arancione */
            font-weight: bold;
            border-top: 1px solid {green_liguria};
            padding-top: 1rem;
        }}
        </style>
    """, unsafe_allow_html=True)

apply_custom_style()

# --- MESSAGGIO INIZIALE DI BUON NATALE ---
if 'christmas_message_shown' not in st.session_state:
    st.session_state.christmas_message_shown = False

if not st.session_state.christmas_message_shown:
    st.empty() # Pulisce lo schermo per il messaggio
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists(pilly_ico_path):
            st.image(pilly_ico_path, use_column_width=True)
        st.markdown(f"<h1 style='text-align:center; color:{orange_req}; font-weight:900;'>BUON NATALE PILLI!!</h1>", unsafe_allow_html=True)
        if st.button("Continua nell'app"):
            st.session_state.christmas_message_shown = True
            st.rerun()
    st.stop() # Ferma l'esecuzione del resto dell'app

# --- Se il messaggio di Natale è stato mostrato, prosegui con l'app ---

# 4. Header
col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
with col_l2:
    if os.path.exists(logo_liguria_path):
        st.image(logo_liguria_path, use_column_width=True)

st.markdown(f"<h1 class='main-title'>📬 EMAIL EXTRACTOR PRO</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='app-subtitle'>REGIONE LIGURIA - GESTIONE LISTE</p>", unsafe_allow_html=True)

# STATO SESSIONE per la logica dell'app
if 'file_caricato' not in st.session_state:
    st.session_state.file_caricato = False
if 'elaborazione_conclusa' not in st.session_state:
    st.session_state.elaborazione_conclusa = False

# STEP 1: CARICAMENTO
if not st.session_state.file_caricato:
    st.markdown(f'<div class="instruction-badge">📂 CARICA IL DOCUMENTO EXCEL</div>', unsafe_allow_html=True)
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
    st.markdown(f'<div class="instruction-badge">🎯 SELEZIONA LA COLONNA EMAIL</div>', unsafe_allow_html=True)
    colonna = st.selectbox("", st.session_state.df.columns, index=min(3, len(st.session_state.df.columns)-1))
    
    st.write("")
    if st.button("🚀 AVVIA ELABORAZIONE DATI"):
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

# STEP 3: RISULTATI
if st.session_state.elaborazione_conclusa:
    st.markdown(f'<div class="instruction-badge">📋 COPIA CON CTRL + A</div>', unsafe_allow_html=True)
    st.text_area(label="", value=st.session_state.risultato, height=180)
    
    m1, m2 = st.columns(2)
    m1.metric("EMAIL UNICHE", st.session_state.count_uniche)
    m2.metric("DUPLICATI RIMOSSI", st.session_state.count_duplicati)
    
    st.divider()
    
    st.markdown(f'<div class="instruction-badge">📥 DOWNLOAD E RESET</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button("SCARICA TXT", data=st.session_state.risultato, file_name="email_pulite.txt")
    with c2:
        st.download_button("SCARICA LOG", data=st.session_state.log, file_name="log_duplicati.txt")
    with c3:
        if st.button("🔄 RE-START"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.christmas_message_shown = False # Resetta il messaggio di Natale
            st.rerun()

st.markdown(f"<div class='footer'>REGIONE LIGURIA</div>", unsafe_allow_html=True)
