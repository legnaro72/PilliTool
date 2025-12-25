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

# 3. CSS Avanzato (Testi Arancione Vivace, Grassetti e UI Dinamica)
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
        /* Pannello centrale opaco ma trasparente sui bordi */
        .main .block-container {
            background-color: rgba(255, 255, 255, 0.95); 
            padding: 3rem;
            border-radius: 30px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.3);
            margin-top: 2rem;
            border: 2px solid #ff6600; /* Bordo arancione sottile */
        }

        /* TITOLI E SCRITTE IN ARANCIONE VIVACE E GRASSETTO */
        h1, h2, h3, p, label, .stMarkdown {
            color: #ff6600 !important; /* Arancione vivace */
            font-weight: bold !important;
        }

        .subtitle { 
            text-align: center; 
            color: #ff6600 !important; 
            font-size: 1.2rem;
            margin-bottom: 2rem; 
            font-weight: bold;
        }
        
        /* Area Upload */
        [data-testid="stFileUploadDropzone"] {
            border: 3px dashed #ff6600 !important;
            background-color: rgba(255, 102, 0, 0.05) !important;
            border-radius: 20px !important;
        }

        /* Bottoni (Verde Istituzionale mantenuto per contrasto o arancione?) 
           Mettiamo un gradiente Arancione/Rosso per i bottoni */
        .stButton>button {
            background: linear-gradient(135deg, #ff6600 0%, #ff4500 100%);
            color: white !important;
            border-radius: 12px;
            padding: 0.8rem;
            font-weight: bold;
            width: 100%;
            border: none;
            font-size: 1.1rem;
        }

        /* Area di testo Risultato */
        textarea {
            border: 2px solid #ff6600 !important;
            background-color: #ffffff !important;
            color: #333 !important;
            font-weight: normal !important; /* Il testo dentro l'area meglio normale per leggibilità */
        }

        /* Footer */
        .footer {
            text-align: center;
            margin-top: 3rem;
            border-top: 1px solid #ff6600;
            padding-top: 1rem;
            color: #ff6600;
        }
        </style>
    """, unsafe_allow_html=True)

apply_custom_style()

# 4. Header Logo
col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
with col_l2:
    if os.path.exists(logo_liguria_path):
        st.image(logo_liguria_path, use_column_width=True)

st.markdown("<h1>📬 EMAIL EXTRACTOR PRO</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Servizio Gestione Liste - Regione Liguria</p>", unsafe_allow_html=True)

# GESTIONE STATO
if 'file_caricato' not in st.session_state:
    st.session_state.file_caricato = False
if 'elaborazione_conclusa' not in st.session_state:
    st.session_state.elaborazione_conclusa = False

# STEP 1: CARICAMENTO (Scompare dopo l'upload)
if not st.session_state.file_caricato:
    st.markdown("### 📤 CARICA IL FILE EXCEL")
    uploaded_file = st.file_uploader("", type="xlsx")
    if uploaded_file is not None:
        try:
            st.session_state.df = pd.read_excel(uploaded_file, engine='openpyxl')
            st.session_state.file_caricato = True
            st.rerun()
        except Exception as e:
            st.error(f"Errore: {e}. Controlla se hai creato il file requirements.txt con 'openpyxl'")

# STEP 2: SCELTA COLONNA (Scompare dopo l'elaborazione)
if st.session_state.file_caricato and not st.session_state.elaborazione_conclusa:
    st.warning("✅ FILE ANALIZZATO CON SUCCESSO")
    
    st.markdown("### 🎯 SELEZIONA LA COLONNA EMAIL")
    colonna = st.selectbox("", st.session_state.df.columns, index=min(3, len(st.session_state.df.columns)-1))
    
    if st.button("🚀 ELABORA E PULISCI DATI"):
        emails_raw = st.session_state.df[colonna].dropna().astype(str)
        seen = set()
        unique_emails = []
        log_entries = [f"--- REPORT {datetime.now().strftime('%H:%M')} ---"]

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

# STEP 3: RISULTATO (Sola visualizzazione finale)
if st.session_state.elaborazione_conclusa:
    st.success("🎉 ELABORAZIONE COMPLETATA")
    
    m1, m2 = st.columns(2)
    with m1: st.metric("EMAIL UNICHE", st.session_state.count_uniche)
    with m2: st.metric("DUPLICATI RIMOSSI", st.session_state.count_duplicati)
    
    st.markdown("### 📋 SELEZIONA TUTTO (CTRL + A) E COPIA")
    st.text_area(label="", value=st.session_state.risultato, height=150)
    
    st.divider()
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button("📥 SCARICA LISTA", data=st.session_state.risultato, file_name="email_pulite.txt")
    with c2:
        st.download_button("🧾 SCARICA LOG", data=st.session_state.log, file_name="log_duplicati.txt")
    with c3:
        if st.button("🔄 NUOVA ANALISI"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# Footer
st.markdown("<div class='footer'><b>REGIONE LIGURIA</b><br>TOOL DIGITALE MAILING LIST</div>", unsafe_allow_html=True)
