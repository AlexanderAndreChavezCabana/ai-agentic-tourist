# Azure App Service Deployment Guide

## 📋 Pasos para Desplegar en Azure

### 1. Preparar cuenta de Azure
- Crear cuenta en [Azure Portal](https://portal.azure.com)
- Suscripción activa (Free Tier disponible)

### 2. Crear App Service desde Azure Portal

1. **Ir a Azure Portal > Create Resource > App Service**

2. **Configuración básica:**
   - Subscription: Tu suscripción
   - Resource Group: Crear nuevo "rg-huaraz-chatbot" 
   - Name: "huaraz-chatbot-ai" (debe ser único)
   - Publish: Code
   - Runtime stack: Python 3.10
   - Operating System: Linux
   - Region: East US (o más cercano)

3. **Plan de precios:**
   - Pricing tier: F1 (Free) o B1 (Basic) para producción

### 3. Configurar Variables de Entorno

En Azure Portal > Tu App Service > Configuration > Application Settings:

```
OPENAI_API_KEY = tu_openai_api_key_aqui
OPENWEATHER_API_KEY = tu_weather_api_key_aqui  
DEFAULT_LLM_PROVIDER = gpt-4o-mini
APP_NAME = Chatbot Turístico Huaraz
DEBUG = false
LOG_LEVEL = INFO
```

### 4. Despliegue desde GitHub (Recomendado)

1. **En Azure Portal > Tu App Service > Deployment Center:**
   - Source: GitHub
   - Authorize Azure to access GitHub
   - Organization: Tu usuario
   - Repository: ai-agentic-tourist
   - Branch: main

2. **GitHub Actions se configurará automáticamente**

### 5. Despliegue Manual (Alternativa)

```bash
# Instalar Azure CLI
pip install azure-cli

# Login a Azure
az login

# Configurar deployment
az webapp deployment source config --name huaraz-chatbot-ai --resource-group rg-huaraz-chatbot --repo-url https://github.com/TuUsuario/ai-agentic-tourist --branch main --manual-integration

# Deploy
az webapp deploy --name huaraz-chatbot-ai --resource-group rg-huaraz-chatbot
```

### 6. Verificar Despliegue

- URL: `https://huaraz-chatbot-ai.azurewebsites.net`
- Logs: Azure Portal > App Service > Log Stream
- Metrics: Azure Portal > App Service > Metrics

### 7. Configuraciones Adicionales en Azure

**En Configuration > General Settings:**
- Python version: 3.10
- Startup Command: `python startup.py`
- Always On: On (para planes de pago)

**En Configuration > Application Settings:**
```
PYTHONPATH = /home/site/wwwroot
WEBSITE_RUN_FROM_PACKAGE = 0
```

### 8. Troubleshooting

**Ver logs en tiempo real:**
```bash
az webapp log tail --name huaraz-chatbot-ai --resource-group rg-huaraz-chatbot
```

**Común errors:**
- ModuleNotFoundError: Verificar requirements.txt
- API Key errors: Verificar variables de entorno
- Port errors: Azure usa variable PORT automáticamente

### 9. Optimizaciones de Producción

**Performance:**
- Habilitar Application Insights
- Configurar CDN para archivos estáticos
- Usar Redis Cache para sessiones

**Security:**
- Configurar Custom Domain + SSL
- Habilitar Authentication si es necesario
- Configurar CORS específicos

## 💰 Costos Estimados

- **Free Tier (F1):** $0/mes (limites: 60 min CPU/día)
- **Basic (B1):** ~$13/mes (24/7 uptime)  
- **Standard (S1):** ~$75/mes (auto-scaling)

## 🚀 Ready to Deploy!

Una vez configurado, tu chatbot estará disponible en:
`https://tu-app-name.azurewebsites.net`