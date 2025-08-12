# 🚀 Guida Deploy Railway - Stratego Swat AI Analyzer

## ✅ Configurazione Completata

Tutti i file di configurazione per Railway sono stati creati:
- `railway.toml` - Configurazione principale Railway
- `railway.json` - Schema JSON alternativo
- `.railwayignore` - File da escludere dal deploy

## 🎯 Passaggi per il Deploy

### 1. Preparazione Repository

```bash
# Assicurati che tutti i file siano committati
git add .
git commit -m "Add Railway configuration"
git push origin main
```

### 2. Deploy su Railway

#### Opzione A: Deploy da GitHub (Raccomandato)

1. **Vai su [Railway.app](https://railway.app)**
2. **Clicca "Start a New Project"**
3. **Seleziona "Deploy from GitHub repo"**
4. **Autorizza Railway ad accedere al tuo GitHub**
5. **Seleziona il repository dell'app**
6. **Railway rileverà automaticamente il Dockerfile**
7. **Il deploy inizierà automaticamente!**

#### Opzione B: Deploy da CLI

```bash
# Installa Railway CLI
npm install -g @railway/cli

# Login
railway login

# Inizializza progetto
railway init

# Deploy
railway up
```

### 3. Configurazione Automatica

Railway configurerà automaticamente:
- ✅ **Docker Build**: Usa il Dockerfile esistente
- ✅ **Playwright**: Browser installati automaticamente
- ✅ **NLTK**: Dati scaricati durante il build
- ✅ **Variabili d'ambiente**: Configurate tramite railway.toml
- ✅ **Porta**: Automaticamente assegnata da Railway
- ✅ **SSL**: Certificato HTTPS automatico

### 4. Monitoraggio Deploy

1. **Dashboard Railway**: Visualizza log di build e deploy
2. **URL automatico**: Railway genera un URL pubblico
3. **Logs in tempo reale**: Monitora l'applicazione
4. **Metriche**: CPU, RAM, traffico

## 🔧 Configurazioni Specifiche

### Risorse Allocate
- **RAM**: 2GB (sufficiente per Playwright)
- **CPU**: 1000m (1 core)
- **Storage**: Automatico
- **Bandwidth**: Illimitato

### Variabili d'Ambiente Configurate
```bash
STREAMLIT_SERVER_HEADLESS=true
PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
NLTK_DATA=/app/nltk_data
PORT=8501
```

### Health Check
- **Path**: `/_stcore/health` (endpoint specifico Streamlit)
- **Timeout**: 300 secondi
- **Retry**: 3 tentativi

## 🎉 Dopo il Deploy

### Verifica Funzionalità
1. **Accedi all'URL generato da Railway**
2. **Testa estrazione AI Overview**
3. **Verifica upload file**
4. **Controlla analisi content gap**
5. **Verifica visualizzazioni Plotly**

### URL dell'App
Dopo il deploy, Railway fornirà un URL tipo:
```
https://your-app-name.railway.app
```

## 🔍 Troubleshooting

### Build Fallisce
- **Controlla logs**: Dashboard Railway > Build Logs
- **Verifica Dockerfile**: Deve essere nella root del progetto
- **Dipendenze**: Controlla requirements.txt

### App Non Si Avvia
- **Porta**: Railway assegna automaticamente $PORT
- **Logs**: Controlla Runtime Logs
- **Health Check**: Verifica che l'app risponda su `/_stcore/health`

### Errore "Service Unavailable" durante Health Check
**Problema**: Railway non riesce a verificare lo stato dell'app
**Causa**: Health check configurato su path sbagliato
**Soluzione**: 
- Streamlit usa `/_stcore/health` come endpoint di health check
- NON usare `/` come path di health check
- La configurazione corretta è già impostata nei file railway.toml e railway.json

### Playwright Non Funziona
- **Browser**: Verificati automaticamente nel Dockerfile
- **Headless**: Configurato automaticamente
- **Dipendenze**: Installate durante il build

## 📊 Vantaggi Railway

- ✅ **Deploy automatico**: Push su GitHub = deploy automatico
- ✅ **Scaling automatico**: Si adatta al traffico
- ✅ **SSL gratuito**: HTTPS automatico
- ✅ **Logs centralizzati**: Monitoraggio completo
- ✅ **Zero configurazione**: Rileva automaticamente tutto
- ✅ **Rollback facile**: Torna a versioni precedenti

## 🎯 Costi

- **Hobby Plan**: $5/mese per progetti personali
- **Pro Plan**: $20/mese per uso professionale
- **Trial gratuito**: 500 ore/mese

## 🔗 Link Utili

- [Railway Dashboard](https://railway.app/dashboard)
- [Railway Docs](https://docs.railway.app/)
- [Railway CLI](https://docs.railway.app/develop/cli)
- [Railway Status](https://status.railway.app/)

---

**✅ CONFIGURAZIONE COMPLETATA!**

Tutti i file necessari sono stati creati. Ora puoi procedere con il deploy su Railway seguendo i passaggi sopra.

**IMPORTANTE**: Il codice dell'applicazione NON è stato modificato - solo aggiunti file di configurazione per Railway.