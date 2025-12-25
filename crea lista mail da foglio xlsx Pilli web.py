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

# 3. CSS Avanzato
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
        .main .block-container {
            background-color: rgba(255, 255, 255, 0.90);
            padding: 2rem;
            border-radius: 25px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            margin-top: 1rem;
        }

        [data-testid="stFileUploadDropzone"] {
            border: 2px dashed #166534 !important;
            background-color: rgba(22, 101, 52, 0.05) !important;
            min-height: 180px;
        }

        h1 { color: #166534 !important; font-size: 1.8rem !important; text-align: center; }
        .subtitle { text-align: center; color: #15803d; font-style: italic; }
        
        /* Stile per le istruzioni di copia */
        .copy-instructions {
            background-color: #f0fdf4;
            border-left: 5px solid #166534;
            padding: 15px;
            border-radius: 8px;
            font-size: 0.95rem;
            color: #14532d;
            margin-bottom: 10px;
        }

        .stButton>button {
            background: linear-gradient(135deg, #166534 0%, #15803d 100%);
            color: white !important;
            border-radius: 12px;
            height: 3.5rem;
            font-weight: bold;
            width: 100%;
        }

        .footer {
            text-align: center;
            margin-top: 2rem;
            font-size: 0.8rem;
            color: #666;
        }
        </style>
    """, unsafe_allow_html=True)

apply_custom_style()

# 4. Header Logo
col_l1, col_l2, col_l3 = st.columns([1, 1.5, 1])
with col_l2:
    if os.path.exists(logo_liguria_path):
        st.image(logo_liguria_path, use_column_width=True)

st.markdown("<h1>📬 EMAIL EXTRACTOR PRO</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Regione Liguria - Gestione Liste</p>", unsafe_allow_html=True)

# --- LOGICA ---
if 'file_elaborato' not in st.session_state:
    st.session_state.file_elaborato = False

# PASSO 1: CARICAMENTO
if 'df' not in st.session_state:
    st.markdown("### 📤 Caricamento Documento")
    uploaded_file = st.file_uploader(
        "Seleziona il file Excel (.xlsx o .xls)", 
        type=["xlsx", "xls"]
    )
    if uploaded_file:
        try:
            st.session_state.df = pd.read_excel(uploaded_file)
            st.rerun()
        except Exception as e:
            st.error(f"Errore nel caricamento del file: {e}")

# PASSO 2: CONFIGURAZIONE
if 'df' in st.session_state and not st.session_state.file_elaborato:
    st.info(f"✅ File caricato: {len(st.session_state.df)} righe.", icon="📂")
    colonna = st.selectbox("Seleziona la colonna email:", st.session_state.df.columns)
    
    if st.button("🚀 ELABORA LISTA"):
        emails_raw = st.session_state.df[colonna].dropna().astype(str)
        seen = set()
        unique_emails = []
        log_entries = [f"--- REPORT {datetime.now().strftime('%H:%M')} ---"]

        for idx, email in emails_raw.items():
            clean_email = email.strip().lower()
            if clean_email in seen:
                log_entries.append(f"❌ Riga {idx+2}: {clean_email}")
            else:
                seen.add(clean_email)
                unique_emails.append(clean_email)
        
        unique_emails.sort(key=lambda x: (x.split("@")[1] if "@" in x else "", x))
        
        st.session_state.risultato = ", ".join(unique_emails)
        st.session_state.log = "\n".join(log_entries)
        st.session_state.count_uniche = len(unique_emails)
        st.session_state.count_duplicati = len(log_entries)-1
        st.session_state.file_elaborato = True
        st.rerun()

# PASSO 3: RISULTATO FINALE
if st.session_state.file_elaborato:
    st.balloons()
    st.success("✨ Elaborazione completata!")
    
    c1, c2 = st.columns(2)
    c1.metric("Email Uniche", st.session_state.count_uniche)
    c2.metric("Duplicati Rimossi", st.session_state.count_duplicati)
    
    # --- NUOVA SEZIONE ISTRUZIONI ---
    st.markdown("### 🎁 LISTA PRONTA! COPIA E INCOLLA")
    st.markdown("""
        <div class="copy-instructions">
            <b>Istruzioni:</b> Clicca nel box qui sotto e premi <b>Ctrl+A</b> per selezionare tutto, 
            poi <b>Ctrl+C</b> per copiare. Infine, vai sul tuo client di posta e premi 
            <b>Ctrl+V</b> per incollare la lista.
        </div>
    """, unsafe_allow_html=True)
    
    st.text_area("Indirizzi pronti:", value=st.session_state.risultato, height=200)
    
    st.divider()
    
    col_dl1, col_dl2, col_dl3 = st.columns(3)
    with col_dl1:
        st.download_button("📥 Scarica TXT", data=st.session_state.risultato, file_name="email_pulite.txt")
    with col_dl2:
        st.download_button("🧾 Scarica Log", data=st.session_state.log, file_name="log_duplicati.txt")
    with col_dl3:
        if st.button("🔄 Nuova Analisi"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

st.markdown('<div class="footer"><b>Regione Liguria</b><br>Tool Digitale Gestione Mailing List</div>', unsafe_allow_html=True)
