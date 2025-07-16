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

### 4. 🎯 Render (Raccomandato per semplicità)

#### Opzione A: Deploy automatico con render.yaml (Raccomandato)

1. **Crea account su [Render](https://render.com)**
2. **Connetti il repository GitHub**
3. **Il file `render.yaml` configurerà automaticamente tutto**
4. **Render rileverà automaticamente la configurazione Docker**

#### Opzione B: Configurazione manuale

1. **Crea nuovo Web Service**
2. **Seleziona "Docker" come ambiente**
3. **Configura il servizio:**
   ```
   Build Command: docker build -t stratego-swat-ai .
   Start Command: docker run -p 8501:8501 stratego-swat-ai
   ```
4. **Variabili d'ambiente:**
   ```
   STREAMLIT_SERVER_HEADLESS=true
   STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
   PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
   ```

#### Troubleshooting Render

- **Se il build fallisce:** Controlla i log di build per errori Playwright
- **Se l'app non si avvia:** Verifica che la porta 8501 sia esposta
- **Se Playwright non funziona:** Assicurati di usare il Dockerfile fornito

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