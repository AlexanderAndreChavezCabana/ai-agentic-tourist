# 🚀 Google Cloud Run Deployment Guide

## ¿Por qué Cloud Run?

- 🐳 **Contenedores nativos** - Tu Dockerfile ya está listo
- ⚡ **Deploy en 2 minutos** - Más rápido que Azure
- 💰 **Pay-per-use real** - Solo pagas cuando recibe requests
- 🔄 **Auto-scaling a 0** - $0 cuando nadie lo usa
- 🌍 **CDN global automático** - Rápido en todo el mundo
- 📊 **Perfecto para FastAPI** - Arquitectura serverless

---

## 🚀 DEPLOYMENT PASO A PASO (5 minutos)

### **Paso 1: Setup Google Cloud**

#### 1.1 Crear cuenta (GRATIS)
- Ve a [Google Cloud Console](https://console.cloud.google.com)
- Registrate (incluye $300 USD gratuitos)
- Crea un proyecto: `huaraz-chatbot` 

#### 1.2 Instalar Google Cloud CLI
```powershell
# Windows - Descargar desde:
# https://cloud.google.com/sdk/docs/install

# O usar chocolatey:
choco install gcloudsdk

# Verificar instalación
gcloud --version
```

#### 1.3 Configurar proyecto
```bash
# Login a Google Cloud
gcloud auth login

# Establecer proyecto
gcloud config set project tu-proyecto-id

# Habilitar Cloud Run API
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

---

### **Paso 2: Configurar Variables de Entorno**

Crea archivo `.env.production`:
```bash
OPENAI_API_KEY=tu_openai_api_key_aqui
DEFAULT_LLM_PROVIDER=openai
APP_NAME=Chatbot Turístico Huaraz
DEBUG=false
LOG_LEVEL=INFO
```

---

### **Paso 3: Deploy con un solo comando** 

```bash
# Deploy directo (Google Cloud Build + Cloud Run)
gcloud run deploy huaraz-chatbot \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="OPENAI_API_KEY=tu_api_key_aqui,DEFAULT_LLM_PROVIDER=openai,DEBUG=false"
```

**¡Eso es todo!** 🎉

---

## ⚡ MÉTODO SÚPER RÁPIDO (Automatizado)

### **Script de Deploy Automático:**

```bash
# Ejecutar script automatizado
python deploy_cloudrun.py
```

**El script hace todo automáticamente:**
- ✅ Verifica dependencias
- ✅ Configura variables de entorno  
- ✅ Construye imagen Docker
- ✅ Despliega a Cloud Run
- ✅ Te da la URL pública

---

## 🌐 RESULTADO

Después del deploy verás:
```
✅ Deployment finished successfully
🌍 Your service is live at: 
https://huaraz-chatbot-abcd123-uc.a.run.app

🔗 Direct chat interface: 
https://huaraz-chatbot-abcd123-uc.a.run.app/static/index.html
```

---

## 💰 COSTOS (MUY BARATOS)

- **Request gratuitos:** 2 millones/mes
- **CPU time gratuito:** 180,000 vCPU-seconds/mes  
- **Memory gratuito:** 360,000 GiB-seconds/mes

### Ejemplo de costos reales:
- **1000 users/día:** ~$2-5/mes
- **Sin usuarios:** $0/mes (auto-scale a 0)
- **Development/testing:** Completamente gratis

---

## 🔧 CONFIGURACIONES AVANZADAS

### **Custom Domain:**
```bash
gcloud run domain-mappings create \
  --service huaraz-chatbot \
  --domain tudominio.com \
  --region us-central1
```

### **Autenticación:**
```bash
# Solo usuarios autenticados
gcloud run deploy huaraz-chatbot \
  --no-allow-unauthenticated
```

### **Scaling configuración:**
```bash
gcloud run deploy huaraz-chatbot \
  --max-instances 10 \
  --concurrency 80 \
  --cpu 1 \
  --memory 2Gi
```

---

## 📊 MONITORING

### **Ver logs en tiempo real:**
```bash
gcloud logging read "resource.type=cloud_run_revision" --limit 50 --format "table(timestamp, textPayload)"
```

### **Métricas en consola:**
- Ve a [Cloud Run Console](https://console.cloud.google.com/run)
- Click en tu servicio → **Metrics** tab
- Ver requests, latency, CPU, memory

---

## 🆘 TROUBLESHOOTING

### **Error: "Port not specified"**
```bash
# El startup.py ya maneja PORT automáticamente
# Verifica que Dockerfile use: CMD ["python", "startup.py"]
```

### **Error: "API Key not set"**
```bash
# Configurar variables de entorno
gcloud run services update huaraz-chatbot \
  --set-env-vars="OPENAI_API_KEY=tu_key_aqui"
```

### **Error: "Memory exceeded"**  
```bash
# Aumentar memoria
gcloud run deploy huaraz-chatbot \
  --memory 2Gi
```

### **Deploy muy lento:**
```bash
# Usar imagen pre-construida
docker build -t gcr.io/tu-proyecto/huaraz-chatbot .
docker push gcr.io/tu-proyecto/huaraz-chatbot
gcloud run deploy --image gcr.io/tu-proyecto/huaraz-chatbot
```

---

## 🔄 CI/CD AUTOMÁTICO

### **GitHub Actions (Optional):**
Crear `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Cloud Run
on:
  push:
    branches: [main]
    
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: google-github-actions/setup-gcloud@v0
    - run: |
        gcloud run deploy huaraz-chatbot \
          --source . \
          --platform managed \
          --region us-central1 \
          --allow-unauthenticated
```

---

## ⚖️ **CLOUD RUN vs AZURE APP SERVICE**

| Característica | Cloud Run | Azure App Service |
|---------------|-----------|------------------|
| **Setup time** | 2 minutos | 10-15 minutos |
| **Costos idle** | $0 | ~$13/mes |
| **Scaling** | 0 → 1000+ automático | Manual/configuración |
| **Docker support** | Nativo | Limitado |
| **FastAPI** | Perfecto | Requiere configuración |
| **Global CDN** | Automático | Manual |
| **Pay model** | Pay-per-use real | Siempre pagando |

**🏆 Veredicto:** Cloud Run es mejor para tu uso case.

---

## 🎯 SIGUIENTE PASOS

1. **Deploy ahora:**
   ```bash
   python deploy_cloudrun.py
   ```

2. **Configurar dominio personalizado**
3. **Agregar monitoring/alerts**  
4. **Setup CI/CD automático**
5. **Optimizar performance**

---

## 📱 COMPARTIR TU CHATBOT

Una vez deployado:
```
🌍 URL pública: https://tu-servicio.a.run.app
📱 Mobile friendly: Funciona perfecto en celulares
🔗 Share: Comparte la URL con cualquier persona
📊 Analytics: Ve métricas en Cloud Console
```

---

**✨ Tu chatbot estará disponible globalmente en minutos, no horas.**

**¿Listo para el deploy más rápido de tu vida?** 🚀

---

**Actualizado:** Febrero 2026  
**Compatibilidad:** Windows/Linux/MacOS  
**Status:** ✅ PRODUCTION READY