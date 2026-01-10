# 🔄 MIGRACIÓN A OPENAI - DOCUMENTACIÓN

## 📋 Resumen de Cambios

**Fecha de migración:** 10 de Enero de 2026  
**Desde:** Google AI (Gemini)  
**Hacia:** OpenAI (GPT-4o)

---

## 🔧 Cambios Realizados

### 1. Dependencias (`requirements.txt`)

**Antes:**
```txt
langchain-google-genai>=0.0.1
```

**Después:**
```txt
langchain-openai>=0.0.5
openai>=1.0.0
```

### 2. Cliente LLM (`src/llm/base.py`)

**Antes:**
```python
from langchain_google_genai import ChatGoogleGenerativeAI

class GoogleAIClient(LLMClient):
    def __init__(self, model_name: str = "gemini-pro", ...):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
    
    def get_model(self):
        return ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=self.api_key
        )
```

**Después:**
```python
from langchain_openai import ChatOpenAI

class OpenAIClient(LLMClient):
    def __init__(self, model_name: str = "gpt-4o", ...):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
    
    def get_model(self):
        return ChatOpenAI(
            model=self.model_name,
            openai_api_key=self.api_key
        )
```

### 3. Configuración del Modelo (`config/model_config.yaml`)

**Antes:**
```yaml
models:
  google:
    provider: "google"
    model_name: "gemini-2.5-flash"
default_model: "google"
```

**Después:**
```yaml
models:
  openai:
    provider: "openai"
    model_name: "gpt-4o"
default_model: "openai"
```

### 4. Variables de Entorno (`.env`)

**Antes:**
```env
GOOGLE_API_KEY=your_google_api_key_here
DEFAULT_LLM_PROVIDER=google
```

**Después:**
```env
OPENAI_API_KEY=your_openai_api_key_here
DEFAULT_LLM_PROVIDER=openai
```

### 5. Código de Aplicación

Actualizado en todos los archivos:
- `main.py` - Proveedor por defecto: `"openai"`
- `examples/basic_usage.py`
- `examples/create_itinerary.py`
- `examples/specialized_queries.py`
- `install.py`

### 6. Documentación

**Archivos actualizados:**
- ✅ `README.md` - Actualizada sección de integraciones
- ✅ `SETUP_OPENAI.md` - Nueva guía de configuración
- ✅ `FINAL_STATUS.md` - Estado actualizado
- 📝 `SETUP_GOOGLE_AI.md` - Conservado para referencia

---

## 🚀 Pasos para Completar la Migración

### 1. Obtener API Key de OpenAI

1. Ve a https://platform.openai.com/api-keys
2. Inicia sesión o crea una cuenta
3. Haz clic en "Create new secret key"
4. Copia la API key

### 2. Actualizar Variables de Entorno

Edita el archivo `.env`:
```env
OPENAI_API_KEY=sk-tu_api_key_aqui
DEFAULT_LLM_PROVIDER=openai
```

### 3. Reinstalar Dependencias

```bash
# Activar entorno virtual
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Reinstalar dependencias
pip install -r requirements.txt --upgrade
```

### 4. Verificar la Instalación

```bash
# Prueba de importación
python test_imports.py

# Prueba del chatbot
python test_chatbot.py

# Ejecutar aplicación
python main.py
```

---

## 📊 Comparación de Modelos

| Característica | Google AI (Gemini) | OpenAI (GPT-4o) |
|----------------|-------------------|-----------------|
| **Modelo por defecto** | gemini-2.5-flash | gpt-4o |
| **Contexto** | ~32K tokens | ~128K tokens |
| **Velocidad** | Muy rápida | Rápida |
| **Costo** | Gratis (limitado) | Pago por uso |
| **Multimodal** | ✅ Sí | ✅ Sí |
| **Idiomas** | ✅ Excelente | ✅ Excelente |

---

## 🔍 Modelos OpenAI Disponibles

### Recomendados para Producción

| Modelo | Descripción | Uso recomendado |
|--------|-------------|-----------------|
| **gpt-4o** | Último GPT-4 optimizado | ⭐ Mejor balance calidad/precio |
| **gpt-4-turbo** | GPT-4 con más contexto | Conversaciones largas |
| **gpt-3.5-turbo** | Más rápido y económico | Desarrollo y testing |

### Cambiar Modelo

Edita `config/model_config.yaml`:
```yaml
models:
  openai:
    model_name: "gpt-4-turbo"  # Cambia aquí
```

O al instanciar:
```python
chatbot = ChatbotTouristico(llm_provider="openai")
# El modelo se lee de model_config.yaml
```

---

## 💰 Consideraciones de Costo

### Precios aproximados (sujetos a cambios)

- **GPT-4o**: ~$2.50 / 1M tokens
- **GPT-4-turbo**: ~$10 / 1M tokens  
- **GPT-3.5-turbo**: ~$0.50 / 1M tokens

### Estimación de uso

Para una conversación típica (10 intercambios):
- Entrada: ~2,000 tokens
- Salida: ~1,500 tokens
- **Costo con GPT-4o**: ~$0.01 USD

### Créditos gratuitos

OpenAI ofrece $5 de crédito inicial para nuevos usuarios (puede variar).

---

## ⚠️ Troubleshooting

### Error: "Incorrect API key provided"

**Solución:**
```bash
# Verifica que tu .env tenga:
OPENAI_API_KEY=sk-...  # Debe empezar con sk-
```

### Error: "You exceeded your current quota"

**Soluciones:**
1. Añadir método de pago en https://platform.openai.com/account/billing
2. Verificar límites en https://platform.openai.com/account/limits
3. Usar GPT-3.5-turbo para testing (más económico)

### Error: "Rate limit exceeded"

**Soluciones:**
1. Esperar unos segundos entre solicitudes
2. Implementar reintentos con backoff exponencial (ya incluido en el código)
3. Actualizar límite de rate en tu cuenta de OpenAI

---

## 📚 Recursos Adicionales

- [Documentación OpenAI](https://platform.openai.com/docs)
- [Guía de precios](https://openai.com/pricing)
- [Playground de OpenAI](https://platform.openai.com/playground)
- [LangChain + OpenAI](https://python.langchain.com/docs/integrations/platforms/openai)
- [SETUP_OPENAI.md](SETUP_OPENAI.md) - Guía de configuración detallada

---

## ✅ Checklist de Migración

- [x] Actualizar `requirements.txt`
- [x] Modificar `src/llm/base.py`
- [x] Actualizar `config/model_config.yaml`
- [x] Configurar `.env` con `OPENAI_API_KEY`
- [x] Actualizar ejemplos en `examples/`
- [x] Actualizar `main.py`
- [x] Crear `SETUP_OPENAI.md`
- [x] Actualizar `README.md`
- [x] Actualizar `FINAL_STATUS.md`
- [ ] Reinstalar dependencias: `pip install -r requirements.txt`
- [ ] Obtener API key de OpenAI
- [ ] Configurar API key en `.env`
- [ ] Probar con `python test_chatbot.py`

---

**Estado:** ✅ Migración completada  
**Próximo paso:** Configurar tu API key de OpenAI y probar el chatbot
