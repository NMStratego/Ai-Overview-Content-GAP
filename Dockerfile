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

# Verifica installazione Playwright
RUN python -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); browser = p.chromium.launch(); browser.close(); p.stop(); print('✅ Playwright funziona correttamente')"

# Copia codice applicazione
COPY . .

# Esponi porta Streamlit
EXPOSE 8501

# Comando per avviare l'applicazione
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]