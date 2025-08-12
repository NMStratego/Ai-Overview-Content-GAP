# Dockerfile per Stratego Swat AI Analyzer con supporto Playwright
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# Imposta directory di lavoro
WORKDIR /app

# Aggiorna sistema e installa dipendenze di sistema necessarie
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libxss1 \
    libnss3 \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements
COPY requirements.txt .

# Installa dipendenze Python
RUN pip install --no-cache-dir -r requirements.txt

# Installa browser Playwright con tutte le dipendenze
RUN playwright install chromium
RUN playwright install-deps chromium

# Imposta variabili d'ambiente per Playwright
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=0

# Verifica che i browser siano installati correttamente
RUN ls -la /ms-playwright/ || echo "Browser path not found, checking alternatives..."
RUN find /usr -name "chrome" -type f 2>/dev/null || echo "Chrome executable not found in /usr"
RUN find /opt -name "chrome" -type f 2>/dev/null || echo "Chrome executable not found in /opt"

# Copia lo script di inizializzazione dipendenze
COPY init_dependencies.py .

# Forza reinstallazione browser se necessario
RUN python3 -c "import subprocess; subprocess.run(['playwright', 'install', 'chromium', '--with-deps'], check=True)"

# Verifica che Playwright funzioni correttamente
RUN python3 -c "from playwright.sync_api import sync_playwright; exec('with sync_playwright() as p: browser = p.chromium.launch(headless=True); page = browser.new_page(); page.goto(\"data:text/html,<h1>Test</h1>\"); print(\"✅ Playwright verification successful\"); page.close(); browser.close()')" || (echo '❌ Playwright verification failed' && exit 1)

# Inizializza tutte le dipendenze (NLTK, ecc.)
RUN python3 init_dependencies.py

# Copia codice applicazione
COPY . .

# Esponi porta Streamlit
EXPOSE 8501

# Imposta variabili d'ambiente per runtime
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
ENV DISPLAY=:99

# Comando per avviare l'applicazione
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8080", "--server.address=0.0.0.0"]