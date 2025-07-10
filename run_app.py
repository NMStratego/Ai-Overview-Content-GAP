#!/usr/bin/env python3
"""
Script di avvio per AI Overview & Content Gap Analyzer
Sviluppata by Nicolas Micolani

Questo script verifica le dipendenze e avvia l'interfaccia Streamlit
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Verifica che tutte le dipendenze siano installate"""
    required_packages = [
        'streamlit',
        'selenium', 
        'requests',
        'beautifulsoup4',
        'nltk',
        'plotly',
        'pandas'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies():
    """Installa le dipendenze mancanti"""
    print("🔧 Installazione dipendenze in corso...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dipendenze installate con successo!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Errore durante l'installazione delle dipendenze")
        return False

def setup_nltk():
    """Configura NLTK scaricando i dati necessari"""
    try:
        import nltk
        print("📚 Download dati NLTK...")
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("✅ Dati NLTK configurati!")
    except Exception as e:
        print(f"⚠️ Avviso: Errore configurazione NLTK: {e}")

def check_chrome():
    """Verifica che Chrome sia installato"""
    chrome_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",  # macOS
        "/usr/bin/google-chrome",  # Linux
        "/usr/bin/chromium-browser",  # Linux Chromium
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",  # Windows
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"  # Windows 32-bit
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            return True
    
    # Prova anche a cercare chrome nel PATH
    try:
        subprocess.run(["chrome", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    try:
        subprocess.run(["google-chrome", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    return False

def main():
    """Funzione principale"""
    print("🚀 AI Overview & Content Gap Analyzer")
    print("   Sviluppata by Nicolas Micolani")
    print("=" * 50)
    
    # Verifica directory corrente
    current_dir = Path.cwd()
    app_file = current_dir / "streamlit_app.py"
    
    if not app_file.exists():
        print("❌ File streamlit_app.py non trovato!")
        print("   Assicurati di essere nella directory corretta.")
        return
    
    # Verifica Chrome
    print("🔍 Verifica installazione Chrome...")
    if not check_chrome():
        print("⚠️ Google Chrome non trovato!")
        print("   Installa Chrome da: https://www.google.com/chrome/")
        print("   Su macOS: brew install --cask google-chrome")
        response = input("   Continuare comunque? (y/n): ")
        if response.lower() != 'y':
            return
    else:
        print("✅ Chrome trovato!")
    
    # Verifica dipendenze
    print("🔍 Verifica dipendenze...")
    missing = check_dependencies()
    
    if missing:
        print(f"❌ Dipendenze mancanti: {', '.join(missing)}")
        response = input("   Installare automaticamente? (y/n): ")
        if response.lower() == 'y':
            if not install_dependencies():
                return
        else:
            print("   Installa manualmente con: pip install -r requirements.txt")
            return
    else:
        print("✅ Tutte le dipendenze sono installate!")
    
    # Setup NLTK
    setup_nltk()
    
    # Avvia Streamlit
    print("\n🌟 Avvio interfaccia web...")
    print("   L'applicazione si aprirà automaticamente nel browser")
    print("   URL: http://localhost:8501")
    print("   Premi Ctrl+C per fermare l'applicazione")
    print("=" * 50)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
    except KeyboardInterrupt:
        print("\n👋 Applicazione fermata dall'utente")
    except Exception as e:
        print(f"\n❌ Errore durante l'avvio: {e}")
        print("   Prova ad avviare manualmente con: streamlit run streamlit_app.py")

if __name__ == "__main__":
    main()