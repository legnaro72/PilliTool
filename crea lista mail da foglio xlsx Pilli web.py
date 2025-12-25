import streamlit as st
import pandas as pd
import base64
import os
from datetime import datetime

# 1. Configurazione della Pagina
st.set_page_config(
    page_title="Email Extractor Pro - Liguria", 
    page_icon="🎄", 
    layout="centered"
)

# --- DEFINIZIONE COLORI GLOBALI ---
orange_req = "rgb(255, 165, 0)"  # Arancione Pilli
green_liguria = "#1E8449"         # Verde Istituzionale Liguria

# 2. Funzioni Base64 (Immagini e Audio)
def get_base64_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

img_bg_base64 = get_base64_file("no.png")
pilly_base64 = get_base64_file("pilli.jpg")
logo_liguria_path = "Logo Liguria.png"
audio_path = "C'e' chi dice no.mp3" # Nome del file audio

# 3. CSS Personalizzato (Stile Originale Pilly)
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
        /* Contenitore principale */
        .main .block-container {{
            background-color: rgba(255, 255, 255, 0.98); 
            padding: 3rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-top: 2rem;
        }}

        /* Titolo Arancione */
        .main-title {{
            color: {orange_req} !important;
            font-weight: 900 !important;
            text-align: center;
            font-size: 3rem !important;
            margin-bottom: 0.5rem;
        }}

        /* Badge Istruzioni */
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
        
        /* Box Istruzioni Copia/Incolla */
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

        /* Bottoni */
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
        
        /* Metriche */
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
        </style>
    """, unsafe_allow_html=True)

apply_custom_style()

# --- MESSAGGIO DI AUGURI INIZIALE ---
if 'christmas_message_shown' not in st.session_state:
    st.session_state.christmas_message_shown = False

if not st.session_state.christmas_message_shown:
    st.snow() 
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if pilly_base64:
            st.markdown(
                f'<div style="text-align: center;"><img src="data:image/jpeg;base64,{pilly_base64}" width="100%" style="border-radius: 25px; border: 5px solid {orange_req}; box-shadow: 0 0 20px {orange_req};"></div>', 
                unsafe_allow_html=True
            )
            
        st.markdown(f"""
            <div style='text-align:center; margin-top:30px;'>
                <h1 style='color:{orange_req}; font-weight:900; font-size: 3.5rem;'>
                    🎅 BUON NATALE PILLI!! 🎄
                </h1>
                <p style='color:{green_liguria}; font-size: 2rem;'>
                    ✨ 🎁 ❄️ 🤶 🦌 ⛄ 🎁 ✨
                </p>
                <p style='color:{orange_req}; font-weight:bold; font-size: 1.2rem;'>
                    Tanti auguri di cuore per un fantastico Natale!
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎁 APRI IL TUO STRUMENTO DI LAVORO 🎁"):
            st.session_state.christmas_message_shown = True
            st.rerun()
    st.stop()

# --- LOGICA AUDIO DI BACKGROUND ---
# Posizioniamo il selettore in alto a destra o nella sidebar
with st.sidebar:
    st.markdown("### 🎵 Controllo Musica")
    audio_enabled = st.checkbox("Attiva Musica 'C'è chi dice no'", value=True)

if audio_enabled:
    audio_b64 = get_base64_file(audio_path)
    if audio_b64:
        # Inseriamo un tag audio HTML invisibile che va in autoplay e loop
        audio_html = f"""
            <audio autoplay loop>
            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
            Your browser does not support the audio element.
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    else:
        st.sidebar.warning(f"File audio '{audio_path}' non trovato.")

# --- INTERFACCIA APP PRINCIPALE ---
col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
with col_l2:
    if os.path.exists(logo_liguria_path):
        st.image(logo_liguria_path, use_column_width=True)

st.markdown(f"<h1 class='main-title'>📬 EMAIL EXTRACTOR PRO</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:{orange_req}; font-weight:bold;'>🎄 REGIONE LIGURIA - MAILING LIST TOOL 🎄</p>", unsafe_allow_html=True)

if 'file_caricato' not in st.session_state:
    st.session_state.file_caricato = False
if 'elaborazione_conclusa' not in st.session_state:
    st.session_state.elaborazione_conclusa = False

# STEP 1: UPLOAD
if not st.session_state.file_caricato:
    st.markdown(f'<div class="instruction-badge">🎅 CARICA IL FILE EXCEL DI NATALE 🎄</div>', unsafe_allow_html=True)
    # Fix per Android: type list estesa
    uploaded_file = st.file_uploader("", type=["xlsx", "xls"])
    if uploaded_file is not None:
        try:
            st.session_state.df = pd.read_excel(uploaded_file)
            st.session_state.file_caricato = True
            st.rerun()
        except Exception as e:
            st.error(f"Errore: {e}")

# STEP 2: SCELTA COLONNA
if st.session_state.file_caricato and not st.session_state.elaborazione_conclusa:
    st.markdown(f'<div class="instruction-badge">❄️ SCEGLI LA COLONNA CON LE EMAIL ❄️</div>', unsafe_allow_html=True)
    colonna = st.selectbox("", st.session_state.df.columns, index=min(3, len(st.session_state.df.columns)-1))
    
    if st.button("🚀 AVVIA ELABORAZIONE"):
        emails_raw = st.session_state.df[colonna].dropna().astype(str)
        seen = set()
        unique_emails = []
        log_entries = [f"REPORT NATALE 2025 - {datetime.now().strftime('%H:%M')}"]

        for idx, email in emails_raw.items():
            clean_email = email.strip().lower()
            if clean_email in seen:
                log_entries.append(f"❌ DUPLICATO ELIMINATO: {clean_email}")
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

# STEP 3: RISULTATI FINALI
if st.session_state.elaborazione_conclusa:
    st.balloons()
    st.markdown(f'<div class="instruction-badge">🎁 LISTA PRONTA! COPIA E INCOLLA 🎁</div>', unsafe_allow_html=True)
    
    # BOX ISTRUZIONI AGGIUNTO
    st.markdown(f"""
        <div class="copy-text-box">
            <b>ISTRUZIONI RAPIDE:</b><br>
            Clicca nella message box qui sotto e premi <b>Control+A</b> per selezionare tutti gli indirizzi email e <b>Control+C</b> per copiarli.<br>
            Vai sul client di posta e premi <b>Control+V</b> per incollare la lista delle mail.
        </div>
    """, unsafe_allow_html=True)

    st.text_area(label="", value=st.session_state.risultato, height=180)
    
    m1, m2 = st.columns(2)
    m1.metric("✨ INDIRIZZI UNICI", st.session_state.count_uniche)
    m2.metric("🚫 DUPLICATI RIMOSSI", st.session_state.count_duplicati)
    
    st.divider()
    
    st.markdown(f'<div class="instruction-badge">📥 SCARICA I DOCUMENTI</div>', unsafe_allow_html=True)
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

st.markdown(f"<div class='footer'>🎅 REGIONE LIGURIA - BUONE FESTE PILLI! 🎄</div>", unsafe_allow_html=True)
