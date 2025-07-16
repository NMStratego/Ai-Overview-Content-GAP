#!/usr/bin/env python3
"""
Ai Analyzer - Interfaccia ultra-moderna per analisi AI Overview e Content Gap
Powered by Nicolas Micolani
"""

# Inizializzazione dipendenze per Render
try:
    from init_dependencies import initialize_all_dependencies
    initialize_all_dependencies()
except ImportError:
    # Se il file non esiste, continua senza inizializzazione
    pass
except Exception as e:
    print(f"⚠️ Avviso inizializzazione dipendenze: {e}")

import streamlit as st
import json
import time
import threading
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from ai_overview_extractor import AIOverviewExtractor
from content_gap_analyzer import ContentGapAnalyzer
from semantic_analyzer import SemanticAnalyzer
import pandas as pd
import io
import base64
import os
import glob

# Configurazione pagina
st.set_page_config(
    page_title="Stratego Ai Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS professionale ed elegante
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Source+Code+Pro:wght@400;500&display=swap');
    
    /* Variabili CSS professionali */
    :root {
        --primary-blue: #2563eb;
        --secondary-blue: #1e40af;
        --accent-blue: #3b82f6;
        --success-green: #059669;
        --warning-orange: #d97706;
        --danger-red: #dc2626;
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --bg-tertiary: #f1f5f9;
        --bg-card: #ffffff;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --text-muted: #94a3b8;
        --border-light: 1px solid #e2e8f0;
        --border-medium: 1px solid #cbd5e1;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    /* Reset e base professionale */
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    .stApp {
        background: var(--bg-secondary);
        min-height: 100vh;
        color: var(--text-primary);
    }
    
    .main .block-container {
        padding: 1rem;
        max-width: 1600px;
    }
    
    /* Header professionale */
    .cyber-header {
        text-align: center;
        padding: 1rem;
        margin-bottom: 2rem;
        animation: slideIn 0.6s ease-out;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0;
    }
    
    .header-logo {
        margin-bottom: 0;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .header-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .cyber-title {
        font-family: 'Inter', sans-serif !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        margin-bottom: 0.5rem !important;
        line-height: 1.2 !important;
    }
    
    .cyber-subtitle {
        font-size: 1.125rem !important;
        font-weight: 400 !important;
        color: var(--text-secondary) !important;
        margin-bottom: 1.5rem !important;
        line-height: 1.6 !important;
    }
    
    .cyber-powered {
        font-family: 'Source Code Pro', monospace !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        color: var(--primary-blue) !important;
    }
    
    /* Cards professionali */
    .cyber-card {
        background: var(--bg-card);
        border: var(--border-light);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-md);
        transition: all 0.2s ease;
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .cyber-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
        border-color: var(--accent-blue);
    }
    
    /* Metric cards professionali */
    .metric-card {
        background: var(--bg-card);
        border: var(--border-light);
        border-left: 4px solid var(--primary-blue);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: var(--shadow-md);
        transition: all 0.2s ease;
        animation: fadeIn 0.5s ease-out;
        margin: 1rem 0;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
        border-left-color: var(--accent-blue);
    }
    
    .metric-value {
        font-family: 'Inter', sans-serif !important;
        font-size: 2.25rem !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        margin-bottom: 0.5rem !important;
        line-height: 1 !important;
    }
    
    .metric-label {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        color: var(--text-secondary) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Benchmark cards */
    .benchmark-card {
        background: var(--bg-card);
        border: var(--border-light);
        border-left: 4px solid var(--success-green);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: var(--shadow-md);
        transition: all 0.2s ease;
        animation: fadeIn 0.5s ease-out;
        margin: 1rem 0;
    }
    
    .benchmark-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
        border-left-color: var(--warning-orange);
    }
    
    .benchmark-value {
        font-family: 'Inter', sans-serif !important;
        font-size: 2.25rem !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        margin-bottom: 0.5rem !important;
        line-height: 1 !important;
    }
    
    .benchmark-label {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        color: var(--text-secondary) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Bottoni professionali */
    .stButton > button {
        background: var(--primary-blue) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        text-transform: none !important;
        letter-spacing: 0.025em !important;
        transition: all 0.2s ease !important;
        box-shadow: var(--shadow-sm) !important;
        cursor: pointer !important;
    }
    
    .stButton > button:hover {
        background: var(--secondary-blue) !important;
        transform: translateY(-1px) !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    /* Input fields professionali */
    .stTextInput > div > div > input {
        background: var(--bg-card) !important;
        border: var(--border-medium) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.75rem !important;
        transition: all 0.2s ease !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-blue) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
        outline: none !important;
    }
    
    /* Sidebar professionale */
    .css-1d391kg {
        background: var(--bg-card) !important;
        border-right: var(--border-light) !important;
    }
    
    /* Tabs professionali */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-tertiary) !important;
        border-radius: 8px !important;
        padding: 0.25rem !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 6px !important;
        color: var(--text-secondary) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        margin: 0 0.125rem !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--bg-card) !important;
        color: var(--primary-blue) !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    /* AI Overview container */
    .ai-overview-container {
        background: var(--bg-card);
        border: var(--border-light);
        border-radius: 12px;
        padding: 2rem;
        box-shadow: var(--shadow-md);
        margin: 1rem 0;
        animation: fadeIn 0.6s ease-out;
    }
    
    .ai-overview-container:hover {
        box-shadow: var(--shadow-lg);
    }
    
    /* Status messages */
    .status-success {
        background: rgba(5, 150, 105, 0.1) !important;
        border: 1px solid var(--success-green) !important;
        color: var(--success-green) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
    }
    
    .status-warning {
        background: rgba(217, 119, 6, 0.1) !important;
        border: 1px solid var(--warning-orange) !important;
        color: var(--warning-orange) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
    }
    
    .status-error {
        background: rgba(220, 38, 38, 0.1) !important;
        border: 1px solid var(--danger-red) !important;
        color: var(--danger-red) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
    }
    
    /* Progress bar professionale */
    .stProgress > div > div > div > div {
        background: var(--primary-blue) !important;
        border-radius: 4px !important;
    }
    
    /* Scrollbar professionale */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-tertiary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--text-muted);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-secondary);
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .cyber-header h1 {
            font-size: 2rem;
        }
        
        .cyber-header {
            padding: 2rem 1.5rem;
        }
        
        .metric-value {
            font-size: 1.875rem;
        }
        
        .cyber-card, .metric-card, .benchmark-card {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Configurazione dimensioni logo
LOGO_HEIGHT = 300  # Modifica questo valore per cambiare le dimensioni del logo (in px)

# Header principale professionale con logo
import base64

try:
    # Carica e codifica il logo in base64
    with open('/Users/niksmic/Desktop/AIOVER+2/Ai-Overview-Content-GAP/image/Logo Stratego  (1).svg', 'rb') as f:
        logo_data = f.read()
    logo_base64 = base64.b64encode(logo_data).decode()
    
    st.markdown(f"""
    <div class="cyber-header">
        <div class="header-logo">
            <img src="data:image/svg+xml;base64,{logo_base64}" alt="Stratego Logo" style="height: {LOGO_HEIGHT}px; width: auto;">
        </div>
        <div class="header-content">
            <h1 class="cyber-title"> STRATEGO SWAT AI ANALYZER</h1>
            <p class="cyber-subtitle">Sistema Professionale di Analisi AI Overview & Content Gap</p>
            <p class="cyber-powered">Analisi intelligente per strategie di contenuto ottimizzate</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
except (FileNotFoundError, Exception) as e:
    # Fallback senza logo se il file non viene trovato o c'è un errore
    st.markdown("""
    <div class="cyber-header">
        <div class="header-content">
            <h1 class="cyber-title"> STRATEGO SWAT AI ANALYZER</h1>
            <p class="cyber-subtitle">Sistema Professionale di Analisi AI Overview & Content Gap</p>
            <p class="cyber-powered">Analisi intelligente per strategie di contenuto ottimizzate</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Inizializzazione session state
if 'ai_overview_data' not in st.session_state:
    st.session_state.ai_overview_data = None
if 'content_gap_data' not in st.session_state:
    st.session_state.content_gap_data = None
if 'gemini_api_key' not in st.session_state:
    st.session_state.gemini_api_key = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'semantic_analyzer' not in st.session_state:
    st.session_state.semantic_analyzer = None
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = {}

# Funzioni di utilità

def create_professional_card(content, title=""):
    """Crea una card professionale per contenuti generali"""
    title_html = f"<h3 style='color: var(--primary-blue); margin-bottom: 1rem; font-family: Inter, sans-serif; font-weight: 600;'>{title}</h3>" if title else ""
    return f"""
    <div class="cyber-card">
        {title_html}
        {content}
    </div>
    """

# Configurazione API Key AI
st.session_state.gemini_api_key = "AIzaSyDXB8Lj2gamg7SEYmxvZ_uEs7JX3RKZ9yY"

# Tabs principali
tab1, tab2, tab3 = st.tabs(["🤖 AI Overview Extractor", "💬 Content Gap Analyzer", "📁 File Manager"])

with tab1:
    st.markdown("""
    <div class="cyber-card">
        <h2 style="color: var(--neon-blue); text-shadow: 0 0 10px var(--neon-blue); font-family: 'Orbitron', monospace; margin-bottom: 2rem;">🤖 ESTRAZIONE INTELLIGENTE AI OVERVIEW</h2>
        <p style="color: var(--text-neon); font-size: 1.2rem; line-height: 1.6;">Estrai automaticamente i contenuti dall'AI Overview di Google per qualsiasi query di ricerca. Il sistema utilizza automazione browser avanzata per ottenere il contenuto completo.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input per la query
    query = st.text_input(
        "🔍 Query di ricerca",
        placeholder="Inserisci la tua query di ricerca...",
        help="Inserisci la query per cui vuoi estrarre l'AI Overview"
    )
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        extract_button = st.button("🚀 ESTRAI AI OVERVIEW", use_container_width=True)
    
    with col2:
        if st.session_state.ai_overview_data:
            clear_button = st.button("🗑️ CANCELLA AI OVERVIEW", use_container_width=True)
            if clear_button:
                st.session_state.ai_overview_data = None
    
    if extract_button and query:
        with st.spinner("🔄 Estrazione AI Overview in corso..."):
            extractor = None
            try:
                # Inizializza l'estrattore con timeout e gestione errori migliorata
                extractor = AIOverviewExtractor(headless=True)
                
                # Estrazione diretta senza threading (risolve problemi greenlet)
                print(f"🚀 Avvio estrazione AI Overview per: {query}")
                result = extractor.extract_ai_overview_from_query(query)
                
                if result and result.get('found', False) and result.get('full_content', ''):
                    # Crea un oggetto compatibile per la visualizzazione
                    ai_overview_data = {
                        'query': query,
                        'ai_overview': result.get('full_content', ''),
                        'found': True,
                        'extraction_time': time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    st.session_state.ai_overview_data = ai_overview_data
                    st.success("✅ AI Overview estratto con successo!")
                else:
                    st.warning("⚠️ Nessun AI Overview trovato per questa query")
                    
            except Exception as e:
                st.error(f"❌ Errore durante l'estrazione: {str(e)}")
                # Log dell'errore per debug
                print(f"ERRORE ESTRAZIONE AI OVERVIEW: {str(e)}")
                import traceback
                print(f"STACK TRACE: {traceback.format_exc()}")
                
            finally:
                # Chiudi sempre l'extractor per rilasciare le risorse
                if extractor is not None:
                    try:
                        extractor.close()
                        print("✅ Risorse browser rilasciate correttamente")
                    except Exception as close_error:
                        print(f"⚠️ Errore chiusura browser: {close_error}")
                        # Forza la chiusura delle risorse
                        try:
                            if hasattr(extractor, 'playwright') and extractor.playwright:
                                extractor.playwright.stop()
                        except:
                            pass
    
    # Visualizzazione risultati AI Overview
    if st.session_state.ai_overview_data:
        st.markdown("""
        <div class="ai-overview-container">
            <h3 style="color: var(--neon-green); text-shadow: 0 0 10px var(--neon-green); font-family: 'Orbitron', monospace; margin-bottom: 1.5rem;">📋 RISULTATO AI OVERVIEW</h3>
        </div>
        """, unsafe_allow_html=True)
        
        data = st.session_state.ai_overview_data
        
        # Query utilizzata
        st.markdown(f"""
        <div class="cyber-card">
            <h4 style="color: var(--neon-purple); text-shadow: 0 0 10px var(--neon-purple); font-family: 'Orbitron', monospace;">🔍 Query:</h4>
            <p style="color: var(--text-neon); font-size: 1.2rem; font-weight: 500;">{data.get('query', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Contenuto AI Overview
        if 'ai_overview' in data and data['ai_overview']:
            st.markdown(f"""
            <div class="cyber-card">
                <h4 style="color: var(--neon-blue); text-shadow: 0 0 10px var(--neon-blue); font-family: 'Orbitron', monospace;">🤖 Contenuto AI Overview:</h4>
                <div style="background: rgba(0, 212, 255, 0.1); border: 1px solid var(--neon-blue); border-radius: 15px; padding: 1.5rem; margin-top: 1rem;">
                    <p style="color: var(--text-neon); font-size: 1.1rem; line-height: 1.6;">{data['ai_overview']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Fonti
        if 'sources' in data and data['sources']:
            st.markdown("""
            <div class="cyber-card">
                <h4 style="color: var(--neon-pink); text-shadow: 0 0 10px var(--neon-pink); font-family: 'Orbitron', monospace;">🔗 Fonti:</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for i, source in enumerate(data['sources'], 1):
                st.markdown(f"""
                <div style="background: rgba(255, 0, 110, 0.1); border: 1px solid var(--neon-pink); border-radius: 15px; padding: 1rem; margin: 0.5rem 0;">
                    <p style="color: var(--neon-pink); font-weight: 600; margin-bottom: 0.5rem;">Fonte {i}:</p>
                    <p style="color: var(--text-neon);"><strong>Titolo:</strong> {source.get('title', 'N/A')}</p>
                    <p style="color: var(--text-neon);"><strong>URL:</strong> <a href="{source.get('url', '#')}" target="_blank" style="color: var(--neon-blue);">{source.get('url', 'N/A')}</a></p>
                </div>
                """, unsafe_allow_html=True)
        
        # Timestamp
        if 'timestamp' in data:
            st.markdown(f"""
            <div class="cyber-card">
                <p style="color: var(--text-neon); font-size: 0.9rem; text-align: center; opacity: 0.8;">⏰ Estratto il: {data['timestamp']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Pulsanti di azione per AI Overview
        st.markdown("""
        <div class="cyber-card">
            <h4 style="color: var(--neon-green); text-shadow: 0 0 10px var(--neon-green); font-family: 'Orbitron', monospace; margin-bottom: 1rem;">🚀 AZIONI DISPONIBILI</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Esporta come JSON
            if st.button("📥 ESPORTA JSON", use_container_width=True, key="export_json"):
                export_data = {
                    'query': data.get('query', ''),
                    'ai_overview': data.get('ai_overview', ''),
                    'sources': data.get('sources', []),
                    'extraction_time': data.get('extraction_time', ''),
                    'found': data.get('found', True),
                    'export_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                json_str = json.dumps(export_data, indent=2, ensure_ascii=False)
                st.download_button(
                    label="💾 Scarica JSON",
                    data=json_str,
                    file_name=f"ai_overview_{data.get('query', 'query').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json",
                    use_container_width=True
                )
        
        with col2:
            # Esporta come TXT
            if st.button("📄 ESPORTA TXT", use_container_width=True, key="export_txt"):
                txt_content = f"""AI OVERVIEW ESTRATTO
{'='*50}

Query: {data.get('query', 'N/A')}
Data Estrazione: {data.get('extraction_time', 'N/A')}

CONTENUTO AI OVERVIEW:
{'-'*30}
{data.get('ai_overview', 'N/A')}

"""
                
                if 'sources' in data and data['sources']:
                    txt_content += "FONTI:\n" + "-"*10 + "\n"
                    for i, source in enumerate(data['sources'], 1):
                        txt_content += f"{i}. {source.get('title', 'N/A')}\n   URL: {source.get('url', 'N/A')}\n\n"
                
                txt_content += f"\nEsportato il: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                
                st.download_button(
                    label="💾 Scarica TXT",
                    data=txt_content,
                    file_name=f"ai_overview_{data.get('query', 'query').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        with col3:
            # Invia al Content Gap Analyzer
            if st.button("🎯 INVIA AL CONTENT GAP ANALYZER", use_container_width=True, key="send_to_analyzer"):
                # Prepara i dati per il Content Gap Analyzer
                if st.session_state.semantic_analyzer is None:
                    st.session_state.semantic_analyzer = SemanticAnalyzer(st.session_state.gemini_api_key)
                
                # Crea un messaggio di benvenuto personalizzato
                ai_content = data.get('ai_overview', '')
                query_text = data.get('query', '')
                
                welcome_message = f"""🎯 **AI Overview caricato automaticamente!**

**Query analizzata:** {query_text}
**Contenuto:** {len(ai_content.split())} parole
**Estratto il:** {data.get('extraction_time', 'N/A')}

Sono pronto ad analizzare questo AI Overview per identificare gap di contenuto e opportunità di miglioramento. Cosa vorresti sapere?

💡 **Suggerimenti di analisi:**
- Analizza i punti chiave mancanti nel mio contenuto
- Identifica opportunità di approfondimento
- Suggerisci una strategia di content gap
- Confronta con i miei contenuti esistenti"""
                
                # Pulisci la chat history e aggiungi il messaggio di benvenuto
                st.session_state.chat_history = [{
                    'role': 'assistant', 
                    'content': welcome_message
                }]
                
                # Salva i dati AI Overview per l'analisi
                st.session_state.ai_overview_data = data
                
                st.success("✅ AI Overview inviato al Content Gap Analyzer!")
                st.info("🔄 Vai al tab 'Content Gap Analyzer' per iniziare l'analisi.")
                
                # Auto-switch al tab Content Gap Analyzer dopo 2 secondi
                time.sleep(1)

with tab2:
    st.markdown("""
    <div class="cyber-card">
        <h2 style="color: var(--neon-purple); text-shadow: 0 0 10px var(--neon-purple); font-family: 'Orbitron', monospace; margin-bottom: 2rem;">💬 CONTENT GAP ANALYZER</h2>
        <p style="color: var(--text-neon); font-size: 1.2rem; line-height: 1.6;">Analizza il gap di contenuto con l'intelligenza artificiale avanzata. Chat interattiva per insights approfonditi.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Verifica API Key
    if not st.session_state.gemini_api_key:
        st.warning("⚠️ Configurazione AI non disponibile.")
    else:
        # Inizializza AI Analyzer se non presente
        if st.session_state.semantic_analyzer is None:
            st.session_state.semantic_analyzer = SemanticAnalyzer(st.session_state.gemini_api_key)
        
        # Chat interface pulita
        st.markdown("""
        <div style="text-align: center; margin: 1rem 0;">
        </div>
        """, unsafe_allow_html=True)
        

        # Caricamento JSON semplificato
        st.subheader("📁 Carica AI Overview JSON")
        uploaded_file = st.file_uploader(
            "Carica il file JSON con l'AI Overview estratto",
            type=['json'],
            key="json_upload",
            help="Carica un file JSON contenente l'AI Overview per iniziare l'analisi"
        )
        
        if uploaded_file:
            try:
                data = json.load(uploaded_file)
                if 'ai_overview' in data or 'full_content' in data:
                    st.session_state.ai_overview_data = data
                    st.success("✅ AI Overview caricato con successo!")
                    # Messaggio automatico di benvenuto
                    welcome_msg = f"Ho caricato l'AI Overview. Contiene {len(data.get('ai_overview', data.get('full_content', '')).split())} parole. Cosa vorresti sapere?"
                    if not st.session_state.chat_history or st.session_state.chat_history[-1]['content'] != welcome_msg:
                        st.session_state.chat_history.append({'role': 'assistant', 'content': welcome_msg})
                else:
                    st.error("❌ File JSON non valido. Deve contenere 'ai_overview' o 'full_content'.")
            except Exception as e:
                st.error(f"❌ Errore nel caricamento: {str(e)}")
        
        # Chat history con design pulito
        if st.session_state.chat_history:
            st.markdown("---")
            for message in st.session_state.chat_history:
                if message['role'] == 'user':
                    st.markdown(f"**👤 Tu:** {message['content']}")
                else:
                    st.markdown(f"**🤖 Stratego AI:** {message['content']}")
                st.markdown("")
            st.markdown("---")
        


        
        # Input semplificato
        user_question = st.text_area(
            "💬 Fai una domanda all'AI:",
            placeholder="Es: Come posso migliorare il mio contenuto basandomi sull'AI Overview estratto?",
            height=80
        )
        
        # Pulsanti azione
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🚀 Invia", type="primary", use_container_width=True):
                if user_question.strip():
                    st.session_state.chat_history.append({'role': 'user', 'content': user_question})
                    
                    with st.spinner("🤖 Analizzando..."):
                        try:
                            context = ""
                            if st.session_state.ai_overview_data:
                                ai_content = st.session_state.ai_overview_data.get('ai_overview', st.session_state.ai_overview_data.get('full_content', ''))
                                context += f"\n\nAI OVERVIEW:\n{ai_content[:1500]}..."
                            
                            full_prompt = f"""Sei un esperto SEO e content strategist. Rispondi in modo professionale e dettagliato.\n\nCONTESTO:{context}\n\nDOMANDA: {user_question}\n\nFornisci una risposta completa e actionable in italiano:"""
                            
                            response = st.session_state.semantic_analyzer.model.generate_content(full_prompt)
                            if response and response.text:
                                st.session_state.chat_history.append({'role': 'assistant', 'content': response.text})
                            else:
                                st.error("❌ Errore nella risposta")
                        except Exception as e:
                            st.error(f"❌ Errore: {str(e)}")
                else:
                    st.warning("⚠️ Inserisci una domanda")
        
        with col2:
            if st.button("📄 Esporta Chat", use_container_width=True):
                if st.session_state.chat_history:
                    # Crea il contenuto del documento
                    chat_content = "# Conversazione Content Gap Analyzer\n\n"
                    chat_content += f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
                    
                    for i, message in enumerate(st.session_state.chat_history, 1):
                        role = "👤 **Utente**" if message['role'] == 'user' else "🤖 **AI Assistant**"
                        chat_content += f"## {role}\n\n{message['content']}\n\n---\n\n"
                    
                    # Offri il download
                    st.download_button(
                        label="💾 Scarica Conversazione",
                        data=chat_content,
                        file_name=f"chat_content_gap_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                else:
                    st.warning("⚠️ Nessuna conversazione da esportare")
        
        with col3:
            if st.button("🗑️ Pulisci Chat", use_container_width=True):
                st.session_state.chat_history = []

with tab3:
    st.markdown("""
    <div class="cyber-card">
        <h2 style="color: var(--neon-blue); text-shadow: 0 0 10px var(--neon-blue); font-family: 'Orbitron', monospace; margin-bottom: 2rem;">🏪 MAGAZZINO FILE ESTRATTI</h2>
        <p style="color: var(--text-neon); font-size: 1.2rem; line-height: 1.6;">Carica i tuoi file AI Overview estratti e inviali direttamente al Content Gap Analyzer per l'analisi.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sezione caricamento file
    st.markdown("""
    <div class="cyber-card">
        <h3 style="color: var(--neon-purple); font-family: 'Orbitron', monospace;">📤 CARICA AI OVERVIEW</h3>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Carica un file JSON con AI Overview estratto",
        type=['json'],
        help="Carica un file JSON contenente dati di AI Overview per l'analisi",
        key="ai_overview_uploader"
    )
    
    # Controlla se stiamo eliminando un file per evitare conflitti
    is_deleting = any(st.session_state.get(f"to_delete_{key.split('_')[-1]}", False) for key in st.session_state.keys() if key.startswith("to_delete_"))
    
    if uploaded_file is not None and not is_deleting:
        # Controlla se questo file è già stato processato in questa sessione
        file_key = f"processed_{uploaded_file.name}_{uploaded_file.size}"
        if not st.session_state.get(file_key, False):
            try:
                # Leggi il file JSON
                file_content = json.loads(uploaded_file.read())
                
                # Verifica che sia un file AI Overview valido
                if 'ai_overview' in file_content or 'full_content' in file_content:
                    # Controlla se il file è già stato caricato per evitare duplicati
                    file_exists = False
                    for existing_id, existing_data in st.session_state.uploaded_files.items():
                        if existing_data['name'] == uploaded_file.name:
                            file_exists = True
                            break
                    
                    if not file_exists:
                        # Salva il file nella sessione permanente con ID univoco
                        import time
                        file_id = f"uploaded_{uploaded_file.name}_{int(time.time() * 1000)}"
                        st.session_state.uploaded_files[file_id] = {
                            'name': uploaded_file.name,
                            'content': file_content,
                            'upload_time': datetime.now().strftime('%d/%m/%Y %H:%M')
                        }
                        
                        st.session_state.ai_overview_data = file_content
                        # Marca il file come processato
                        st.session_state[file_key] = True
                        st.success(f"✅ {uploaded_file.name} caricato nel magazzino!")
                    else:
                        st.warning(f"⚠️ {uploaded_file.name} è già presente nel magazzino!")
                        
                else:
                    st.error("❌ File JSON non valido. Deve contenere dati di AI Overview.")
            except json.JSONDecodeError:
                st.error("❌ Errore nel leggere il file JSON. Verifica che sia un file JSON valido.")
            except Exception as e:
                st.error(f"❌ Errore nel caricare il file: {str(e)}")
    
    # Mostra i file caricati salvati nella sessione
    if st.session_state.uploaded_files:
        st.markdown("""
        <div class="cyber-card">
            <h3 style="color: var(--neon-blue); font-family: 'Orbitron', monospace;">📋 FILE CARICATI</h3>
        </div>
        """, unsafe_allow_html=True)
        
        for file_id, file_data in st.session_state.uploaded_files.items():
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                content = file_data['content'].get('ai_overview', file_data['content'].get('full_content', ''))
                word_count = len(content.split()) if content else 0
                query = file_data['content'].get('query', 'N/A')
                
                st.markdown(f"""
                <div style="background: rgba(0, 212, 255, 0.1); border: 1px solid var(--neon-blue); border-radius: 10px; padding: 0.8rem; margin: 0.5rem 0;">
                    <p style="color: var(--neon-blue); margin: 0; font-weight: bold;">📄 {file_data['name']}</p>
                    <p style="color: var(--text-neon); margin: 0.2rem 0; font-size: 0.9rem;">Query: {query[:50]}{'...' if len(query) > 50 else ''}</p>
                    <p style="color: var(--text-neon); margin: 0; font-size: 0.8rem;">Parole: {word_count} | Caricato: {file_data['upload_time']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("🚀 Usa", key=f"use_uploaded_file_{file_id}", help=f"Carica {file_data['name']} e invia al Content Gap Analyzer", use_container_width=True):
                    # Salva i dati immediatamente
                    st.session_state.ai_overview_data = file_data['content']
                    
                    # Prepara messaggio per Content Gap Analyzer
                    content = file_data['content'].get('ai_overview', file_data['content'].get('full_content', ''))
                    word_count = len(content.split())
                    
                    welcome_message = f"""
🎯 **AI Overview caricato dal magazzino!**

**File:** {file_data['name']}
**Query:** {file_data['content'].get('query', 'N/A')}
**Contenuto:** {word_count} parole
**Caricato il:** {file_data['upload_time']}

💡 **Pronto per l'analisi!** Inserisci l'URL di un articolo da confrontare o fai una domanda specifica.
                    """
                    
                    # Inizializza chat history se non esiste
                    if 'chat_history' not in st.session_state:
                        st.session_state.chat_history = []
                    
                    # Aggiungi il messaggio
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': welcome_message
                    })
                    
                    # Mostra conferma con timestamp
                    import datetime
                    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                    st.success(f"✅ {file_data['name']} caricato e inviato al Content Gap Analyzer! ({timestamp})")
                    st.info("🔄 Vai al tab 'Content Gap Analyzer' per iniziare l'analisi.")
            
            with col3:
                # Usa callback con session state per gestire l'eliminazione
                delete_key = f"delete_file_{file_id}"
                if st.button("🗑️", key=delete_key, help=f"Rimuovi {file_data['name']} dal magazzino", use_container_width=True):
                    # Imposta flag di eliminazione nel session state
                    st.session_state[f"to_delete_{file_id}"] = True
                
                # Controlla se c'è un file da eliminare
                if st.session_state.get(f"to_delete_{file_id}", False):
                    if file_id in st.session_state.uploaded_files:
                        file_name = st.session_state.uploaded_files[file_id]['name']
                        del st.session_state.uploaded_files[file_id]
                        # Rimuovi il flag di eliminazione
                        del st.session_state[f"to_delete_{file_id}"]
                        st.success(f"✅ {file_name} rimosso dal magazzino!")
                    else:
                        # Rimuovi il flag anche se il file non esiste
                        if f"to_delete_{file_id}" in st.session_state:
                            del st.session_state[f"to_delete_{file_id}"]
                        st.error(f"❌ Errore: file non trovato nel magazzino!")
    
    # Sezione file locali nel magazzino
    st.markdown("""
    <div class="cyber-card">
        <h3 style="color: var(--neon-pink); font-family: 'Orbitron', monospace;">💾 MAGAZZINO LOCALE</h3>
    </div>
    """, unsafe_allow_html=True)
    
    import os
    import glob
    
    # Cerca file JSON nella directory corrente
    json_files = glob.glob("*.json")
    ai_overview_files = []
    
    # Filtra solo i file AI Overview
    for file in json_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = json.load(f)
                if 'ai_overview' in content or 'full_content' in content:
                    ai_overview_files.append(file)
        except:
            continue
    
    if ai_overview_files:
        for file in ai_overview_files:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        file_content = json.load(f)
                    
                    query = file_content.get('query', 'Query non disponibile')
                    content = file_content.get('ai_overview', file_content.get('full_content', ''))
                    word_count = len(content.split()) if content else 0
                    
                    st.markdown(f"""
                    <div style="background: rgba(179, 71, 217, 0.1); border: 1px solid var(--neon-purple); border-radius: 10px; padding: 0.8rem; margin: 0.5rem 0;">
                        <p style="color: var(--neon-purple); margin: 0; font-weight: bold;">📄 {file}</p>
                        <p style="color: var(--text-neon); margin: 0.2rem 0; font-size: 0.9rem;">Query: {query[:50]}{'...' if len(query) > 50 else ''}</p>
                        <p style="color: var(--text-neon); margin: 0; font-size: 0.8rem;">Parole: {word_count}</p>
                    </div>
                    """, unsafe_allow_html=True)
                except:
                    st.markdown(f"📄 {file} (errore lettura)")
            
            with col2:
                # Pulsante riutilizzabile per invio multiplo
                button_key = f"use_local_file_{file}_{hash(file)}"
                if st.button("🚀 Usa", key=button_key, help=f"Carica {file} e invia al Content Gap Analyzer", use_container_width=True):
                    try:
                        with open(file, 'r', encoding='utf-8') as f:
                            file_content = json.load(f)
                        
                        # Salva i dati immediatamente
                        st.session_state.ai_overview_data = file_content
                        
                        # Prepara messaggio per Content Gap Analyzer
                        content = file_content.get('ai_overview', file_content.get('full_content', ''))
                        word_count = len(content.split())
                        
                        welcome_message = f"""
🎯 **AI Overview caricato dal magazzino locale!**

**File:** {file}
**Query:** {file_content.get('query', 'N/A')}
**Contenuto:** {word_count} parole
**Estratto il:** {file_content.get('extraction_time', 'N/A')}

💡 **Pronto per l'analisi!** Inserisci l'URL di un articolo da confrontare o fai una domanda specifica.
                        """
                        
                        # Inizializza chat history se non esiste
                        if 'chat_history' not in st.session_state:
                            st.session_state.chat_history = []
                        
                        # Aggiungi il messaggio (sempre, anche se già presente)
                        st.session_state.chat_history.append({
                            'role': 'assistant',
                            'content': welcome_message
                        })
                        
                        # Mostra conferma con timestamp per distinguere invii multipli
                        import datetime
                        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                        st.success(f"✅ {file} caricato e inviato al Content Gap Analyzer! ({timestamp})")
                        st.info("🔄 Vai al tab 'Content Gap Analyzer' per iniziare l'analisi.")
                        
                    except Exception as e:
                        st.error(f"❌ Errore nel caricare {file}: {str(e)}")

# Footer
st.markdown("""
<div style="text-align: center; padding: 1rem 1rem 0 1rem; margin-top: 3rem; border-top: 1px solid var(--border-light); color: var(--text-muted);">
    <p style="margin: 0; font-size: 1rem;">© 2025 Stratego Swat | <span class="cyber-powered"><strong>Stratego Swat AI Analyzer V1.0</strong></span> | Sviluppata da <span class="cyber-powered"><strong>Nicolas Micolani</strong></span></p>
</div>
""", unsafe_allow_html=True)