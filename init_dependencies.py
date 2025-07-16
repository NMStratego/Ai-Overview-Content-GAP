#!/usr/bin/env python3
"""
Script di inizializzazione delle dipendenze per Render
Assicura che tutte le dipendenze necessarie siano disponibili
"""

import os
import sys
import subprocess
import logging

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_nltk_data():
    """Scarica i dati NLTK necessari"""
    logger.info("📚 Download dati NLTK...")
    try:
        import nltk
        
        # Crea directory NLTK se non esiste
        nltk_data_dir = os.path.expanduser('~/nltk_data')
        os.makedirs(nltk_data_dir, exist_ok=True)
        
        # Download dei dati necessari
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('punkt_tab', quiet=True)  # Nuovo tokenizer
        
        logger.info("✅ Dati NLTK scaricati con successo")
        return True
    except Exception as e:
        logger.error(f"❌ Errore nel download NLTK: {e}")
        return False

def verify_playwright_installation():
    """Verifica che Playwright sia installato correttamente"""
    logger.info("🎭 Verifica installazione Playwright...")
    try:
        from playwright.sync_api import sync_playwright
        
        # Test di base per verificare che Playwright funzioni
        with sync_playwright() as p:
            # Verifica che i browser siano disponibili
            browser_path = p.chromium.executable_path
            if os.path.exists(browser_path):
                logger.info(f"✅ Playwright Chromium trovato: {browser_path}")
                return True
            else:
                logger.warning(f"⚠️ Browser Chromium non trovato: {browser_path}")
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
    """Inizializza tutte le dipendenze necessarie"""
    logger.info("🚀 Inizializzazione dipendenze per Render...")
    logger.info("=" * 50)
    
    success_count = 0
    total_checks = 6
    
    # Download dati NLTK
    if download_nltk_data():
        success_count += 1
    
    # Verifica Playwright
    if verify_playwright_installation():
        success_count += 1
    
    # Verifica Google Generative AI
    if verify_google_generativeai():
        success_count += 1
    
    # Verifica scikit-learn
    if verify_sklearn():
        success_count += 1
    
    # Verifica Streamlit
    if verify_streamlit_dependencies():
        success_count += 1
    
    # Verifica web scraping
    if verify_web_scraping_dependencies():
        success_count += 1
    
    logger.info("=" * 50)
    logger.info(f"✅ Inizializzazione completata: {success_count}/{total_checks} verifiche riuscite")
    
    if success_count == total_checks:
        logger.info("🎉 Tutte le dipendenze sono pronte!")
        return True
    else:
        logger.warning(f"⚠️ {total_checks - success_count} dipendenze hanno problemi")
        return False

if __name__ == "__main__":
    initialize_all_dependencies()