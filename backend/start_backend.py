#!/usr/bin/env python3
"""
Script di avvio per il backend AI Analyzer
Installa le dipendenze e avvia il server Flask
"""

import subprocess
import sys
import os

def install_requirements():
    """Installa le dipendenze Python"""
    print("📦 Installazione dipendenze Python...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dipendenze installate con successo")
    except subprocess.CalledProcessError as e:
        print(f"❌ Errore nell'installazione delle dipendenze: {e}")
        return False
    return True

def install_playwright():
    """Installa i browser per Playwright"""
    print("🎭 Installazione browser Playwright...")
    try:
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        print("✅ Browser Playwright installati")
    except subprocess.CalledProcessError as e:
        print(f"❌ Errore nell'installazione di Playwright: {e}")
        return False
    return True

def download_nltk_data():
    """Scarica i dati NLTK necessari"""
    print("📚 Download dati NLTK...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("✅ Dati NLTK scaricati")
    except Exception as e:
        print(f"❌ Errore nel download NLTK: {e}")
        return False
    return True

def start_server():
    """Avvia il server Flask"""
    print("🚀 Avvio server AI Analyzer...")
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Errore nell'avvio del server: {e}")
        return False
    return True

def main():
    """Funzione principale"""
    print("🤖 AI Analyzer Backend Setup")
    print("=" * 50)
    
    # Cambia directory al backend
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)
    
    # Installa dipendenze
    if not install_requirements():
        sys.exit(1)
    
    # Installa Playwright
    if not install_playwright():
        print("⚠️ Playwright non installato, alcune funzioni potrebbero non funzionare")
    
    # Download dati NLTK
    if not download_nltk_data():
        print("⚠️ Dati NLTK non scaricati, alcune funzioni potrebbero non funzionare")
    
    print("\n" + "=" * 50)
    print("✅ Setup completato!")
    print("🌐 Frontend: http://localhost:5173")
    print("🔧 Backend API: http://localhost:5000")
    print("=" * 50)
    
    # Avvia il server
    start_server()

if __name__ == "__main__":
    main()