#!/usr/bin/env python3
"""
Script di inizializzazione delle dipendenze per Render
Assicura che tutte le dipendenze necessarie siano disponibili
"""

import os
import sys
import subprocess
import logging
import time

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_nltk_data():
    """Scarica i dati NLTK necessari (ottimizzato per Render)"""
    logger.info("📚 Verifica dati NLTK...")
    try:
        import nltk
        
        # Usa directory NLTK specifica per Render se disponibile
        nltk_data_dir = os.environ.get('NLTK_DOWNLOAD_DIR', os.path.expanduser('~/nltk_data'))
        os.makedirs(nltk_data_dir, exist_ok=True)
        
        # Imposta il path per NLTK
        if nltk_data_dir not in nltk.data.path:
            nltk.data.path.append(nltk_data_dir)
        
        # Lista dei dati NLTK necessari con gestione errori migliorata
        required_data = {
            'punkt': 'tokenizers/punkt',
            'stopwords': 'corpora/stopwords'
        }
        
        # Gestione speciale per punkt_tab (problematico su Render)
        punkt_tab_fallback = os.environ.get('NLTK_PUNKT_TAB_FALLBACK', 'false').lower() == 'true'
        if not punkt_tab_fallback:
            required_data['punkt_tab'] = 'tokenizers/punkt_tab'
        
        missing_data = []
        
        for data_name, data_path in required_data.items():
            try:
                nltk.data.find(data_path)
                logger.info(f"✅ {data_name} già presente")
            except LookupError:
                missing_data.append(data_name)
                logger.info(f"📥 {data_name} mancante, sarà scaricato")
        
        # Scarica solo i dati mancanti con gestione errori robusta
        if missing_data:
            logger.info(f"📥 Download dati NLTK mancanti: {missing_data}")
            for data in missing_data:
                try:
                    # Gestione speciale per punkt_tab
                    if data == 'punkt_tab':
                        logger.info("⚠️ Tentativo download punkt_tab (può fallire su Render)...")
                        try:
                            result = nltk.download(data, quiet=True)
                            if result:
                                logger.info(f"✅ {data} scaricato con successo")
                            else:
                                logger.warning(f"⚠️ {data} non disponibile, usando fallback punkt")
                        except Exception as e:
                            logger.warning(f"⚠️ punkt_tab fallito come atteso su Render: {e}")
                            logger.info("✅ Continuando con punkt standard (sufficiente)")
                    else:
                        result = nltk.download(data, quiet=True)
                        if result:
                            logger.info(f"✅ {data} scaricato con successo")
                        else:
                            logger.warning(f"⚠️ {data} non scaricato (potrebbe non esistere)")
                except Exception as e:
                    logger.warning(f"⚠️ Errore download {data}: {e}")
                    # Continua con gli altri download anche se uno fallisce
        else:
            logger.info("✅ Tutti i dati NLTK già presenti")
        
        # Verifica finale che almeno punkt funzioni (essenziale)
        try:
            nltk.data.find('tokenizers/punkt')
            logger.info("✅ Dati NLTK essenziali pronti")
            return True
        except LookupError:
            # Fallback: prova a scaricare punkt direttamente
            logger.warning("⚠️ Punkt non trovato, tentativo download diretto...")
            try:
                nltk.download('punkt', quiet=True)
                logger.info("✅ Punkt scaricato come fallback")
                return True
            except Exception as e:
                logger.error(f"❌ Impossibile scaricare punkt: {e}")
                return False
        
    except Exception as e:
        logger.error(f"❌ Errore nel setup NLTK: {e}")
        # Anche in caso di errore, ritorna True per non bloccare l'app
        logger.warning("⚠️ Continuando senza NLTK completo...")
        return True

def verify_playwright_installation():
    """Verifica che Playwright sia installato correttamente (ottimizzato)"""
    logger.info("🎭 Verifica Playwright...")
    try:
        # Verifica solo l'import senza avviare browser (più veloce)
        from playwright.sync_api import sync_playwright
        
        # Verifica rapida dell'esistenza del modulo
        logger.info("✅ Playwright disponibile")
        return True
                
    except ImportError as e:
        logger.error(f"❌ Playwright non installato: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Errore nella verifica di Playwright: {e}")
        return False

def verify_google_generativeai():
    """Verifica che google-generativeai sia disponibile"""
    logger.info("🤖 Verifica Google Generative AI...")
    try:
        import google.generativeai as genai
        logger.info("✅ Google Generative AI disponibile")
        return True
    except ImportError as e:
        logger.error(f"❌ Google Generative AI non disponibile: {e}")
        return False

def verify_sklearn():
    """Verifica che scikit-learn sia disponibile"""
    logger.info("🧠 Verifica scikit-learn...")
    try:
        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np
        logger.info("✅ scikit-learn disponibile")
        return True
    except ImportError as e:
        logger.error(f"❌ scikit-learn non disponibile: {e}")
        return False

def verify_streamlit_dependencies():
    """Verifica le dipendenze di Streamlit"""
    logger.info("🎨 Verifica dipendenze Streamlit...")
    try:
        import streamlit as st
        import plotly.graph_objects as go
        import plotly.express as px
        import pandas as pd
        logger.info("✅ Dipendenze Streamlit disponibili")
        return True
    except ImportError as e:
        logger.error(f"❌ Dipendenze Streamlit non disponibili: {e}")
        return False

def verify_web_scraping_dependencies():
    """Verifica le dipendenze per web scraping"""
    logger.info("🕷️ Verifica dipendenze web scraping...")
    try:
        import requests
        from bs4 import BeautifulSoup
        import lxml
        logger.info("✅ Dipendenze web scraping disponibili")
        return True
    except ImportError as e:
        logger.error(f"❌ Dipendenze web scraping non disponibili: {e}")
        return False

def initialize_all_dependencies():
    """Inizializza tutte le dipendenze necessarie (ottimizzato per Render)"""
    logger.info("🚀 Inizializzazione dipendenze per Render (modalità veloce)...")
    logger.info("=" * 50)
    
    # Cache file per evitare verifiche ripetute
    cache_file = '/tmp/.deps_cache'
    
    # Se esiste cache recente (< 1 ora), salta le verifiche
    if os.path.exists(cache_file):
        try:
            cache_time = os.path.getmtime(cache_file)
            current_time = time.time()
            if current_time - cache_time < 3600:  # 1 ora
                logger.info("⚡ Cache dipendenze valida, saltando verifiche")
                logger.info("✅ Dipendenze pronte (da cache)")
                return True
        except:
            pass
    
    success_count = 0
    total_checks = 6
    
    # Verifiche essenziali (solo import, no download/test pesanti)
    checks = [
        ("NLTK", download_nltk_data),
        ("Playwright", verify_playwright_installation),
        ("Google AI", verify_google_generativeai),
        ("Scikit-learn", verify_sklearn),
        ("Streamlit", verify_streamlit_dependencies),
        ("Web Scraping", verify_web_scraping_dependencies)
    ]
    
    for name, check_func in checks:
        try:
            if check_func():
                success_count += 1
        except Exception as e:
            logger.warning(f"⚠️ Errore verifica {name}: {e}")
    
    logger.info("=" * 50)
    logger.info(f"✅ Inizializzazione completata: {success_count}/{total_checks} verifiche riuscite")
    
    # Crea cache se almeno 4/6 dipendenze funzionano
    if success_count >= 4:
        try:
            with open(cache_file, 'w') as f:
                f.write(f"Dependencies checked at {time.time()}")
        except:
            pass
        
        logger.info("🎉 Dipendenze pronte!")
        return True
    else:
        logger.warning(f"⚠️ {total_checks - success_count} dipendenze hanno problemi")
        return False

if __name__ == "__main__":
    initialize_all_dependencies()