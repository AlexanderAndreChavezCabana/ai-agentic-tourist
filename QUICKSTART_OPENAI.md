# ⚡ INICIO RÁPIDO - DESPUÉS DE LA MIGRACIÓN A OPENAI

## 🎯 Pasos Inmediatos

### 1️⃣ Obtén tu OpenAI API Key

👉 https://platform.openai.com/api-keys

1. Inicia sesión en OpenAI
2. Click en "Create new secret key"
3. Copia la clave (empieza con `sk-...`)

### 2️⃣ Configura tu .env

Abre el archivo `.env` y reemplaza:

```env
OPENAI_API_KEY=sk-tu_clave_real_aqui
```

### 3️⃣ Reinstala las dependencias

```bash
# Activa el entorno virtual si no está activo
venv\Scripts\activate

# Reinstala con las nuevas dependencias
pip install -r requirements.txt --upgrade
```

### 4️⃣ Prueba el chatbot

```bash
python main.py
```

---

## ✅ ¡Listo!

Tu chatbot ahora usa **OpenAI GPT-4o** en lugar de Google AI.

### 📊 Diferencias principales:

| Aspecto | Antes (Google AI) | Ahora (OpenAI) |
|---------|-------------------|----------------|
| **Modelo** | Gemini 2.5 Flash | GPT-4o |
| **API Key** | GOOGLE_API_KEY | OPENAI_API_KEY |
| **Costo** | Gratis (limitado) | $2.50/1M tokens |
| **Contexto** | 32K tokens | 128K tokens |

---

## 📚 Más información

- Ver [MIGRATION_OPENAI.md](MIGRATION_OPENAI.md) para detalles completos
- Ver [SETUP_OPENAI.md](SETUP_OPENAI.md) para guía de configuración

---

## ⚠️ ¿Problemas?

**Error: "Incorrect API key"**
→ Verifica que tu API key esté correcta en `.env`

**Error: "You exceeded your quota"**
→ Añade un método de pago en https://platform.openai.com/account/billing

**¿Quieres usar un modelo más económico?**
→ Cambia `gpt-4o` por `gpt-3.5-turbo` en [config/model_config.yaml](config/model_config.yaml)
