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
    """Scarica i dati NLTK necessari (ottimizzato)"""
    logger.info("📚 Verifica dati NLTK...")
    try:
        import nltk
        
        # Crea directory NLTK se non esiste
        nltk_data_dir = os.path.expanduser('~/nltk_data')
        os.makedirs(nltk_data_dir, exist_ok=True)
        
        # Controlla se i dati sono già presenti prima di scaricare
        required_data = ['punkt', 'stopwords', 'punkt_tab']
        missing_data = []
        
        for data in required_data:
            try:
                nltk.data.find(f'tokenizers/{data}')
            except LookupError:
                try:
                    nltk.data.find(f'corpora/{data}')
                except LookupError:
                    missing_data.append(data)
        
        # Scarica solo i dati mancanti
        if missing_data:
            logger.info(f"📥 Download dati NLTK mancanti: {missing_data}")
            for data in missing_data:
                nltk.download(data, quiet=True)
        else:
            logger.info("✅ Dati NLTK già presenti")
        
        logger.info("✅ Dati NLTK pronti")
        return True
    except Exception as e:
        logger.error(f"❌ Errore nel setup NLTK: {e}")
        return False

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