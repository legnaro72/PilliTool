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

# 3. CSS Avanzato (Migliorata leggibilità e visibilità sfondo)
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
        /* Pannello centrale: aumentata opacità per contrastare lo sfondo molto visibile */
        .main .block-container {
            background-color: rgba(255, 255, 255, 0.94); 
            padding: 3rem;
            border-radius: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            margin-top: 2rem;
            border: 1px solid rgba(22, 101, 52, 0.2);
        }

        h1 { color: #166534 !important; font-weight: 800 !important; text-align: center; }
        .subtitle { text-align: center; color: #15803d; font-style: italic; margin-bottom: 2rem; }
        
        /* Area Upload */
        [data-testid="stFileUploadDropzone"] {
            border: 2px dashed #166534 !important;
            background-color: rgba(255, 255, 255, 0.5) !important;
            border-radius: 15px !important;
        }

        /* Bottoni */
        .stButton>button {
            background: linear-gradient(135deg, #166534 0%, #15803d 100%);
            color: white !important;
            border-radius: 12px;
            padding: 0.8rem;
            font-weight: bold;
            width: 100%;
            border: none;
        }

        /* Footer */
        .footer {
            text-align: center;
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 1px solid rgba(0,0,0,0.1);
            color: #444;
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
st.markdown("<p class='subtitle'>Regione Liguria - Elaborazione Liste Contatti</p>", unsafe_allow_html=True)

# --- GESTIONE STATO SESSIONE ---
if 'file_caricato' not in st.session_state:
    st.session_state.file_caricato = False
if 'elaborazione_conclusa' not in st.session_state:
    st.session_state.elaborazione_conclusa = False

# STEP 1: CARICAMENTO (Scompare dopo il caricamento)
if not st.session_state.file_caricato:
    st.markdown("### 📤 Caricamento Documento")
    uploaded_file = st.file_uploader("Trascina qui il tuo file Excel (.xlsx)", type="xlsx")
    if uploaded_file is not None:
        st.session_state.df = pd.read_excel(uploaded_file)
        st.session_state.file_caricato = True
        st.rerun()

# STEP 2: CONFIGURAZIONE (Scompare dopo il click su Elabora)
if st.session_state.file_caricato and not st.session_state.elaborazione_conclusa:
    st.info(f"✅ File caricato: {len(st.session_state.df)} righe rilevate.", icon="📂")
    
    colonna = st.selectbox("Seleziona la colonna delle Email:", st.session_state.df.columns, index=min(3, len(st.session_state.df.columns)-1))
    
    if st.button("🚀 ELABORA E GENERA LISTA"):
        # Logica di estrazione
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
        
        # Salvataggio dati finali
        st.session_state.risultato = ", ".join(unique_emails)
        st.session_state.log = "\n".join(log_entries)
        st.session_state.count_uniche = len(unique_emails)
        st.session_state.count_duplicati = len(log_entries)-1
        st.session_state.elaborazione_conclusa = True
        st.rerun()

# STEP 3: RISULTATO FINALE
if st.session_state.elaborazione_conclusa:
    st.balloons()
    st.success("✨ Lista Email pronta!")
    
    c1, c2 = st.columns(2)
    c1.metric("Email Uniche", st.session_state.count_uniche)
    c2.metric("Duplicati Rimossi", st.session_state.count_duplicati)
    
    st.markdown("### 📋 Seleziona tutto (CTRL + A) e copia")
    st.text_area(label="Indirizzi pronti per l'invio:", value=st.session_state.risultato, height=150)
    
    st.divider()
    
    # Pulsanti Download
    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        st.download_button("📥 Scarica Lista", data=st.session_state.risultato, file_name="email_pulite.txt")
    with col_d2:
        st.download_button("🧾 Scarica Log", data=st.session_state.log, file_name="log_duplicati.txt")
    with col_d3:
        if st.button("🔄 Nuova Analisi"):
            # Reset totale
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# Footer
st.markdown("<div class='footer'><b>Regione Liguria</b><br>Tool Digitale Mailing List</div>", unsafe_allow_html=True)
