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

# 3. CSS Avanzato (Arancione Ultra-Vivace e Grassetto Ovunque)
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
    
    st.markdown(bg_style + """
        <style>
        /* Pannello centrale con opacità per massima leggibilità */
        .main .block-container {
            background-color: rgba(255, 255, 255, 0.96); 
            padding: 3rem;
            border-radius: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
            margin-top: 2rem;
            border: 3px solid #FF4500; /* Arancione Neon */
        }

        /* CONFIGURAZIONE TESTI ARANCIONE VIVACE E GRASSETTO */
        /* Colore esadecimale #FF4500 è l'arancione-rosso più visibile (OrangeRed) */
        
        h1, h2, h3, h4, p, label, .stMarkdown, span, .stMetric, div[data-testid="stMetricValue"] {
            color: #FF4500 !important; 
            font-weight: 900 !important; /* Grassetto massimo */
            opacity: 1 !important;
        }

        /* Titolo principale più grande e marcato */
        .main-title {
            font-size: 3rem !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
            text-align: center;
            line-height: 1.2;
        }

        .subtitle { 
            text-align: center; 
            font-size: 1.4rem !important;
            margin-bottom: 2.5rem; 
            text-transform: uppercase;
        }
        
        /* Area Upload Stilizzata Arancione */
        [data-testid="stFileUploadDropzone"] {
            border: 4px dashed #FF4500 !important;
            background-color: rgba(255, 69, 0, 0.08) !important;
            border-radius: 20px !important;
        }
        
        /* Icone e testi dentro l'upload */
        [data-testid="stFileUploadDropzone"] i, [data-testid="stFileUploadDropzone"] div {
            color: #FF4500 !important;
            font-weight: bold !important;
        }

        /* Bottoni Arancione Fluorescente */
        .stButton>button {
            background: linear-gradient(135deg, #FF4500 0%, #FF8C00 100%);
            color: white !important;
            border-radius: 15px;
            padding: 1rem;
            font-weight: 900 !important;
            width: 100%;
            border: none;
            font-size: 1.2rem;
            letter-spacing: 1px;
            box-shadow: 0 4px 15px rgba(255, 69, 0, 0.4);
        }

        /* Input Selectbox e Textarea */
        .stSelectbox div, textarea {
            border: 2px solid #FF4500 !important;
            font-weight: bold !important;
            color: #333 !important; /* Testo inserito scuro per leggerlo bene */
        }

        /* Footer */
        .footer {
            text-align: center;
            margin-top: 3rem;
            border-top: 2px solid #FF4500;
            padding-top: 1.5rem;
            letter-spacing: 1px;
        }
        </style>
    """, unsafe_allow_html=True)

apply_custom_style()

# 4. Header Logo
col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
with col_l2:
    if os.path.exists(logo_liguria_path):
        st.image(logo_liguria_path, use_column_width=True)

st.markdown("<h1 class='main-title'>📬 EMAIL EXTRACTOR PRO</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>REGIONE LIGURIA - ELABORAZIONE LISTE CONTATTI</p>", unsafe_allow_html=True)

# GESTIONE STATO SESSIONE
if 'file_caricato' not in st.session_state:
    st.session_state.file_caricato = False
if 'elaborazione_conclusa' not in st.session_state:
    st.session_state.elaborazione_conclusa = False

# STEP 1: CARICAMENTO (Scompare dopo l'invio)
if not st.session_state.file_caricato:
    st.markdown("### 📤 CARICA IL DOCUMENTO EXCEL")
    uploaded_file = st.file_uploader("", type="xlsx")
    if uploaded_file is not None:
        try:
            st.session_state.df = pd.read_excel(uploaded_file, engine='openpyxl')
            st.session_state.file_caricato = True
            st.rerun()
        except Exception as e:
            st.error(f"ERRORE CRITICO: {e}. VERIFICA IL FILE REQUIREMENTS.TXT")

# STEP 2: CONFIGURAZIONE (Scompare dopo l'elaborazione)
if st.session_state.file_caricato and not st.session_state.elaborazione_conclusa:
    st.markdown("### ✅ FILE ANALIZZATO: SCEGLI LA COLONNA")
    colonna = st.selectbox("", st.session_state.df.columns, index=min(3, len(st.session_state.df.columns)-1))
    
    st.write("")
    if st.button("🚀 AVVIA ELABORAZIONE DATI"):
        emails_raw = st.session_state.df[colonna].dropna().astype(str)
        seen = set()
        unique_emails = []
        log_entries = [f"--- REPORT {datetime.now().strftime('%H:%M')} ---"]

        for idx, email in emails_raw.items():
            clean_email = email.strip().lower()
            if clean_email in seen:
                log_entries.append(f"❌ RIGA {idx+2}: {clean_email} (DUPLICATO)")
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

# STEP 3: RISULTATO (Visualizzazione finale dinamica)
if st.session_state.elaborazione_conclusa:
    st.balloons()
    st.markdown("## 🎊 ELABORAZIONE COMPLETATA!")
    
    m1, m2 = st.columns(2)
    m1.metric("EMAIL UNICHE", st.session_state.count_uniche)
    m2.metric("DUPLICATI RIMOSSI", st.session_state.count_duplicati)
    
    st.markdown("### 📋 SELEZIONA TUTTO (CTRL + A) E COPIA")
    st.text_area(label="", value=st.session_state.risultato, height=150)
    
    st.divider()
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button("📥 SCARICA LISTA", data=st.session_state.risultato, file_name="email_pulite.txt")
    with c2:
        st.download_button("🧾 SCARICA LOG", data=st.session_state.log, file_name="log_errori.txt")
    with c3:
        if st.button("🔄 NUOVA ANALISI"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# Footer
st.markdown(
    """
    <div class="footer">
        <b>REGIONE LIGURIA</b><br>
        <b>SISTEMA GESTIONE MAILING LIST ISTITUZIONALE</b>
    </div>
    """, 
    unsafe_allow_html=True
)
