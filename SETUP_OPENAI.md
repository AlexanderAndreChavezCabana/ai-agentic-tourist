# ⚙️ CONFIGURACIÓN OPENAI - PASOS RÁPIDOS

## 1️⃣ Obtener tu OpenAI API Key

### Opción A: Crear una nueva API Key
1. Ve a https://platform.openai.com/api-keys
2. Inicia sesión o crea una cuenta en OpenAI
3. Haz clic en "Create new secret key"
4. Dale un nombre a tu API key (ej: "Chatbot Huaraz")
5. Copia la API key generada (solo se mostrará una vez)

### Opción B: Usar una API Key existente
1. Accede a https://platform.openai.com/api-keys
2. Encuentra tu API key existente
3. Si no la recuerdas, crea una nueva

## 2️⃣ Configurar el .env

```bash
# Crear archivo .env basado en el template
cp .env.example .env

# Editar .env y añadir tu API key
# Windows: notepad .env
# Linux/Mac: nano .env
```

Contenido del archivo `.env`:
```
OPENAI_API_KEY=sk-your_api_key_here
DEBUG=false
LOG_LEVEL=INFO
DEFAULT_LLM_PROVIDER=openai
```

## 3️⃣ Instalar dependencias

```bash
# Asegúrate de tener el entorno virtual activado
pip install -r requirements.txt
```

## 4️⃣ Probar la instalación

```bash
# Prueba básica
python test_imports.py

# Prueba completa con OpenAI
python test_chatbot.py

# Ejecutar chatbot interactivo
python main.py
```

## 📝 Modelos Disponibles

### GPT-4 (Recomendado)
- `gpt-4o` - Último modelo GPT-4 optimizado (más rápido y económico)
- `gpt-4-turbo` - Modelo GPT-4 Turbo con mayor contexto
- `gpt-4` - Modelo GPT-4 original

### GPT-3.5
- `gpt-3.5-turbo` - Modelo más rápido y económico

Para cambiar el modelo, edita `config/model_config.yaml`:
```yaml
models:
  openai:
    provider: "openai"
    model_name: "gpt-4o"  # Cambia aquí
    temperature: 0.7
    max_tokens: 2048
```

## 💰 Costos y Límites

- **Cuenta gratuita**: $5 de crédito inicial (para nuevos usuarios)
- **Cuenta de pago**: Pago por uso según el modelo

Precios aproximados (sujetos a cambios):
- GPT-4o: ~$2.50 / 1M tokens
- GPT-3.5-turbo: ~$0.50 / 1M tokens

Más info: https://openai.com/pricing

## 🔧 Troubleshooting

### Error: "Incorrect API key provided"
- Verifica que tu API key esté correctamente copiada en `.env`
- Asegúrate de que no haya espacios adicionales
- La API key debe empezar con `sk-`

### Error: "You exceeded your current quota"
- Has agotado tus créditos
- Añade un método de pago en https://platform.openai.com/account/billing

### Error: "Rate limit exceeded"
- Estás haciendo demasiadas solicitudes
- Espera unos segundos e intenta de nuevo
- Considera actualizar tu plan para límites mayores

## 🌐 Recursos Adicionales

- [Documentación oficial de OpenAI](https://platform.openai.com/docs)
- [Guía de API de OpenAI](https://platform.openai.com/docs/api-reference)
- [Playground de OpenAI](https://platform.openai.com/playground) - Prueba modelos en tu navegador
