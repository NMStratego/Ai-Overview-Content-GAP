# Dockerfile per Stratego Swat AI Analyzer con supporto Playwright
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# Imposta directory di lavoro
WORKDIR /app

# Copia requirements
COPY requirements.txt .

# Installa dipendenze Python
RUN pip install --no-cache-dir -r requirements.txt

# Installa browser Playwright
RUN playwright install chromium
RUN playwright install-deps

# Copia codice applicazione
COPY . .

# Esponi porta Streamlit
EXPOSE 8501

# Comando per avviare l'applicazione
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]