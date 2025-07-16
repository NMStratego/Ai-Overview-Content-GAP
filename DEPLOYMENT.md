# 🚀 Guida al Deployment - Stratego Swat AI Analyzer

## ⚠️ Problema Streamlit Cloud

Streamlit Cloud **NON supporta Playwright** perché non permette l'installazione di browser per motivi di sicurezza.

## 🔧 Soluzioni Alternative

### 1. 🐳 Docker (Raccomandato)

#### Deployment Locale
```bash
# Clona il repository
git clone https://github.com/NiksHacks/Ai-Overview-Content-GAP.git
cd Ai-Overview-Content-GAP

# Avvia con Docker Compose
docker-compose up -d

# Accedi all'app su http://localhost:8501
```

#### Build manuale Docker
```bash
# Build immagine
docker build -t stratego-swat-ai .

# Run container
docker run -p 8501:8501 stratego-swat-ai
```

### 2. 🚀 Heroku

```bash
# Installa Heroku CLI
# Crea app Heroku
heroku create your-app-name

# Aggiungi buildpack Playwright
heroku buildpacks:add --index 1 https://github.com/mxschmitt/heroku-playwright-buildpack.git
heroku buildpacks:add --index 2 heroku/python

# Deploy
git push heroku main
```

### 3. 🌐 Railway

1. Vai su [Railway.app](https://railway.app)
2. Connetti il repository GitHub
3. Railway rileverà automaticamente il Dockerfile
4. Deploy automatico!

### 4. 🎯 Render

1. Vai su [Render.com](https://render.com)
2. Crea nuovo "Web Service"
3. Connetti repository GitHub
4. Usa queste impostazioni:
   - **Build Command**: `pip install -r requirements.txt && playwright install chromium`
   - **Start Command**: `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`

### 5. ☁️ Servizi Cloud Alternativi

#### ScrapingBee
- Sostituisci Playwright con API ScrapingBee
- Supporta JavaScript rendering
- Piano gratuito disponibile

#### Browserless
- Servizio browser cloud
- API compatibile con Playwright
- Ottimo per automazione

## 🔧 Configurazione Ambiente

### Variabili d'Ambiente
```bash
# Per deployment production
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# Per API keys (opzionale)
GOOGLE_API_KEY=your_api_key_here
```

### File .env (per sviluppo locale)
```bash
# Crea file .env
echo "GOOGLE_API_KEY=your_api_key" > .env
```

## 📋 Checklist Pre-Deploy

- [ ] ✅ Requirements.txt aggiornato
- [ ] ✅ Dockerfile presente
- [ ] ✅ Variabili d'ambiente configurate
- [ ] ✅ Repository pushato su GitHub
- [ ] ✅ Piattaforma di deploy scelta

## 🆘 Troubleshooting

### Errore "Executable doesn't exist"
- ❌ **Causa**: Browser Playwright non installati
- ✅ **Soluzione**: Usa Docker o piattaforme che supportano Playwright

### Errore di memoria
- ❌ **Causa**: Browser consuma molta RAM
- ✅ **Soluzione**: Aumenta memoria del container o usa headless mode

### Timeout durante scraping
- ❌ **Causa**: Sito lento o popup non gestiti
- ✅ **Soluzione**: Aumenta timeout o migliora gestione popup

## 📞 Supporto

Per problemi di deployment:
1. Controlla i log del container/servizio
2. Verifica che tutte le dipendenze siano installate
3. Testa localmente con Docker prima del deploy

---

**Sviluppato da Nicolas Micolani** | **Stratego Swat AI Analyzer V1.0**