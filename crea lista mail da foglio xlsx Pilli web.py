import streamlit as st
import pandas as pd
import base64
import os
import io
from datetime import datetime
import msoffcrypto

# 1. Configurazione della Pagina
st.set_page_config(
    page_title="Email Extractor Pro - Pilli by MassiTuo",
    page_icon="🎄",
    layout="centered"
)

# --- DEFINIZIONE COLORI GLOBALI ---
orange_req = "rgb(255, 165, 0)"
green_liguria = "#1E8449"

# 2. Funzione generica per codificare file (Immagini e Audio) in Base64
def get_base64_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

img_bg_base64 = get_base64_file("no.png")
pilly_base64 = get_base64_file("pilli.jpg")
audio_base64 = get_base64_file("C'e' chi dice no.mp3")
logo_liguria_path = "Logo Liguria.png"

# 3. CSS Personalizzato
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

    st.markdown(bg_style + f"""
        <style>
        .main .block-container {{
            background-color: rgba(255, 255, 255, 0.78);
            padding: 3rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-top: 2rem;
        }}
        .main-title {{
            color: {orange_req} !important;
            font-weight: 900 !important;
            text-align: center;
            font-size: 3rem !important;
            margin-bottom: 0.5rem;
        }}
        .instruction-badge {{
            background-color: {green_liguria} !important;
            border: 2px solid {orange_req};
            padding: 12px 20px;
            border-radius: 10px;
            color: {orange_req} !important;
            font-weight: 900;
            margin-bottom: 20px;
            text-transform: uppercase;
            display: block;
            text-align: center;
        }}
        .copy-text-box {{
            background-color: #fff8e1;
            border-left: 6px solid {orange_req};
            padding: 15px;
            margin-bottom: 10px;
            color: #d97706;
            font-size: 0.95rem;
            border-radius: 5px;
            line-height: 1.5;
        }}
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
        [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
            color: {orange_req} !important;
            font-weight: 900 !important;
        }}
        .footer {{
            text-align: center;
            margin-top: 3rem;
            color: {orange_req};
            font-weight: bold;
            border-top: 1px solid {green_liguria};
            padding-top: 1rem;
        }}
        [data-testid="stSidebar"] {{
            background-color: rgba(255, 255, 255, 0.9);
            border-right: 2px solid {orange_req};
        }}
        </style>
    """, unsafe_allow_html=True)

apply_custom_style()

# --- AUDIO ---
if audio_base64:
    with st.sidebar:
        st.markdown(f"<h3 style='color:{orange_req}; text-align:center;'>🎵 MUSIC PLAYER</h3>", unsafe_allow_html=True)
        audio_on = st.toggle("🔊 C'è chi dice no (Vasco)", value=True)
        if audio_on:
            audio_html = f"""
                <audio autoplay loop>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)

# --- STATO SESSIONE ---
if 'file_caricato' not in st.session_state:
    st.session_state.file_caricato = False
if 'elaborazione_conclusa' not in st.session_state:
    st.session_state.elaborazione_conclusa = False

# --- INTERFACCIA ---
st.markdown(f"<h1 class='main-title'>📬 EMAIL EXTRACTOR PRO</h1>", unsafe_allow_html=True)

# STEP 1: UPLOAD + PASSWORD
if not st.session_state.file_caricato:
    st.markdown(f'<div class="instruction-badge">🎅 CARICA IL FILE EXCEL 🎄</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("", type=["xlsx", "xls"])
    password = st.text_input("🔐 Password file Excel (lascia vuoto se non protetto)", type="password")

    if uploaded_file is not None:
        try:
            if password.strip() == "":
                df = pd.read_excel(uploaded_file)
            else:
                decrypted = io.BytesIO()
                office_file = msoffcrypto.OfficeFile(uploaded_file)
                office_file.load_key(password=password)
                office_file.decrypt(decrypted)
                decrypted.seek(0)
                df = pd.read_excel(decrypted)

            st.session_state.df = df
            st.session_state.file_caricato = True
            st.rerun()

        except Exception as e:
            st.error("❌ Errore apertura file. Password errata o file non valido.")
            st.stop()

# STEP 2: SCELTA COLONNA
if st.session_state.file_caricato and not st.session_state.elaborazione_conclusa:
    st.markdown(f'<div class="instruction-badge">❄️ SCEGLI LA COLONNA CON LE EMAIL ❄️</div>', unsafe_allow_html=True)

    colonna = st.selectbox("", st.session_state.df.columns)

    if st.button("🚀 AVVIA ELABORAZIONE"):
        emails_raw = st.session_state.df[colonna].dropna().astype(str)

        seen = set()
        unique_emails = []
        log_entries = [f"REPORT - {datetime.now().strftime('%H:%M')}"]

        for email in emails_raw:
            clean_email = email.strip().lower()
            if clean_email in seen:
                log_entries.append(f"DUPLICATO ELIMINATO: {clean_email}")
            else:
                seen.add(clean_email)
                unique_emails.append(clean_email)

        unique_emails.sort(key=lambda x: (x.split("@")[1] if "@" in x else "", x))

        st.session_state.risultato = ", ".join(unique_emails)
        st.session_state.log = "\n".join(log_entries)
        st.session_state.count_uniche = len(unique_emails)
        st.session_state.count_duplicati = len(log_entries) - 1
        st.session_state.elaborazione_conclusa = True
        st.rerun()

# STEP 3: RISULTATI
if st.session_state.elaborazione_conclusa:
    st.markdown(f'<div class="instruction-badge">🎁 LISTA PRONTA! 🎁</div>', unsafe_allow_html=True)

    st.text_area(label="", value=st.session_state.risultato, height=180)

    m1, m2 = st.columns(2)
    m1.metric("✨ INDIRIZZI UNICI", st.session_state.count_uniche)
    m2.metric("🚫 DUPLICATI RIMOSSI", st.session_state.count_duplicati)

    st.divider()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button("💾 SALVA LISTA", data=st.session_state.risultato, file_name="email_pulite.txt")
    with c2:
        st.download_button("🧾 SALVA LOG", data=st.session_state.log, file_name="log_duplicati.txt")
    with c3:
        if st.button("🔄 NUOVA ANALISI"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

st.markdown(f"<div class='footer'>🎅 BUONE FESTE PILLI! DA MASSITUO 🎄</div>", unsafe_allow_html=True)
