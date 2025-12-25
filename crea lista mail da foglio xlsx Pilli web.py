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

# 3. CSS ORIGINALE RIPRISTINATO + Integrazioni
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
        /* Pannello centrale originale */
        .main .block-container {
            background-color: rgba(255, 255, 255, 0.85);
            padding: 3rem;
            border-radius: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            margin-top: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.4);
        }

        /* Titoli Istituzionali */
        h1 { color: #166534 !important; font-weight: 800 !important; text-align: center; }
        .subtitle { text-align: center; color: #15803d; font-style: italic; margin-bottom: 2rem; }
        
        /* Area Upload (Ottimizzata per Android ma con tuo stile) */
        [data-testid="stFileUploadDropzone"] {
            border: 2px dashed #166534 !important;
            background-color: rgba(22, 101, 52, 0.05) !important;
            border-radius: 15px !important;
            padding: 2rem !important;
        }

        /* Bottoni Originali */
        .stButton>button {
            background: linear-gradient(135deg, #166534 0%, #15803d 100%);
            color: white !important;
            border-radius: 12px;
            padding: 0.8rem;
            font-weight: bold;
            width: 100%;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(22, 101, 52, 0.3);
        }

        /* Box Istruzioni Arancione/Istituzionale */
        .copy-instructions {
            background-color: #fff7ed;
            border-left: 5px solid #f97316; /* Arancione vivace */
            padding: 15px;
            border-radius: 8px;
            font-size: 0.95rem;
            color: #7c2d12;
            margin-bottom: 10px;
            line-height: 1.4;
        }

        /* Box di testo Risultato Originale */
        textarea {
            background-color: #ffffff !important;
            color: #1e293b !important;
            font-family: 'Consolas', monospace !important;
            border: 2px solid #166534 !important;
            border-radius: 10px !important;
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

# --- LOGICA DI NAVIGAZIONE ---
if 'file_elaborato' not in st.session_state:
    st.session_state.file_elaborato = False

# PASSO 1: CARICAMENTO (Con supporto esteso Android)
if 'df' not in st.session_state:
    st.markdown("### 📤 Caricamento Documento")
    uploaded_file = st.file_uploader("Trascina qui il tuo file Excel istituzionale", type=["xlsx", "xls"])
    if uploaded_file:
        st.session_state.df = pd.read_excel(uploaded_file)
        st.rerun()

# PASSO 2: CONFIGURAZIONE
if 'df' in st.session_state and not st.session_state.file_elaborato:
    st.info(f"✅ File pronto: {len(st.session_state.df)} righe rilevate.", icon="📂")
    st.markdown("### 🎯 Selezione Colonna")
    colonna = st.selectbox("Scegli la colonna che contiene gli indirizzi:", st.session_state.df.columns)
    
    if st.button("🚀 ELABORA E GENERA LISTA"):
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
    st.success("✨ Elaborazione completata con successo!")
    
    col_res1, col_res2 = st.columns(2)
    col_res1.metric("Email Uniche", st.session_state.count_uniche)
    col_res2.metric("Duplicati Rimossi", st.session_state.count_duplicati)
    
    st.markdown("### 🎁 LISTA PRONTA! COPIA E INCOLLA")
    # Inserimento del box istruzioni con lo stile arancione richiesto
    st.markdown("""
        <div class="copy-instructions">
            💡 <b>Procedura veloce:</b> Clicca nella message box qui sotto e premi <b>Control+A</b> per selezionare tutti gli indirizzi, 
            poi <b>Control+C</b> per copiarli. Vai sul tuo client di posta e premi <b>Control+V</b> per incollare la lista.
        </div>
    """, unsafe_allow_html=True)
    
    st.text_area(label="Indirizzi pronti per l'invio:", value=st.session_state.risultato, height=150)
    
    st.divider()
    
    c1, c2, c3 = st.columns([1,1,1])
    with c1:
        st.download_button("📥 Scarica Lista", data=st.session_state.risultato, file_name="email_pulite.txt")
    with c2:
        st.download_button("🧾 Scarica Log", data=st.session_state.log, file_name="log_duplicati.txt")
    with c3:
        if st.button("🔄 Nuova Elaborazione"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# Footer
st.markdown(
    """
    <div class="footer">
        <b>Regione Liguria</b><br>
        <i>Tool Digitale per la Gestione Mailing List by MasiTuo</i>
    </div>
    """, 
    unsafe_allow_html=True
)
