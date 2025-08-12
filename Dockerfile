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

# Configurazione Playwright per Railway
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=0
ENV PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=true

# Installa browser Playwright con tutte le dipendenze
RUN playwright install chromium
RUN playwright install-deps chromium

# Verifica installazione browser
RUN ls -la /ms-playwright/ || echo "Browser path not found"
RUN find /ms-playwright -name "chrome" -type f || echo "Chrome executable not found"

# Copia lo script di inizializzazione dipendenze
COPY init_dependencies.py .

# Forza reinstallazione browser se necessario per entrambe le piattaforme
RUN python3 -c "import subprocess; subprocess.run(['playwright', 'install', 'chromium', '--with-deps'], check=True)"

# Imposta variabili d'ambiente per Railway
ENV PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/ms-playwright/chromium-*/chrome-linux/chrome
ENV DISPLAY=:99

# Verifica che Playwright funzioni correttamente
RUN python3 -c "from playwright.sync_api import sync_playwright; exec('with sync_playwright() as p: browser = p.chromium.launch(headless=True); page = browser.new_page(); page.goto(\"data:text/html,<h1>Test</h1>\"); print(\"✅ Playwright verification successful\"); page.close(); browser.close()')" || (echo '❌ Playwright verification failed' && find /ms-playwright -name 'chrome' -type f && exit 1)

# Inizializza tutte le dipendenze (NLTK, ecc.)
RUN python3 init_dependencies.py

# Copia codice applicazione
COPY . .

# Esponi porta per Railway (usa variabile PORT dinamica)
EXPOSE 8080

# Imposta variabili d'ambiente per runtime Railway
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
ENV PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=true
ENV DISPLAY=:99
ENV PORT=8080

# Comando per avviare l'applicazione su Railway
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.headless=true", "--server.enableCORS=false"]