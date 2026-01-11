# 🌐 INTERFAZ WEB - CHATBOT TURÍSTICO HUARAZ

## 🚀 Inicio Rápido

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar API Key

Asegúrate de que tu archivo `.env` tenga tu OpenAI API key:

```env
OPENAI_API_KEY=sk-tu_clave_aqui
```

### 3. Iniciar el Servidor

```bash
python app.py
```

O con uvicorn directamente:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 4. Abrir en el Navegador

```
http://localhost:8000
```

---

## 📚 Documentación de la API

Una vez iniciado el servidor, accede a:

- **Interfaz Web**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

---

## 🎨 Características de la Interfaz

### ✨ Diseño Moderno
- 🏔️ Tema inspirado en la Cordillera Blanca
- 🎨 Gradientes y efectos visuales modernos
- 📱 Responsive design (móvil, tablet, desktop)
- 🌓 Modo oscuro/claro
- ✨ Animaciones suaves y partículas interactivas

### 💬 Chat Interactivo
- 🔌 WebSocket para comunicación en tiempo real
- 💬 Interfaz de chat moderna estilo messenger
- ⚡ Indicador de escritura
- 📤 Exportar conversaciones
- 🔄 Múltiples sesiones de chat
- 🎯 Botones de acciones rápidas

### 🏔️ Explorador de Atracciones
- 📋 Grid de tarjetas con todas las atracciones
- 🔍 Filtros por dificultad (fácil, moderado, difícil)
- 🖼️ Imágenes y descripciones
- 📊 Información de altitud y duración
- 🖱️ Click para preguntar sobre la atracción

### 📊 Estadísticas en Tiempo Real
- 💬 Total de conversaciones
- 📨 Mensajes procesados
- 🟢 Conexiones activas
- 🔄 Actualización automática cada 10 segundos

---

## 🔧 Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno y rápido
- **WebSockets** - Comunicación bidireccional en tiempo real
- **Uvicorn** - Servidor ASGI de alto rendimiento
- **LangChain** - Framework para aplicaciones con LLMs
- **OpenAI GPT-4o** - Modelo de lenguaje

### Frontend
- **HTML5** - Estructura semántica
- **CSS3** - Diseño moderno con variables CSS y gradientes
- **JavaScript (Vanilla)** - Lógica interactiva
- **Particles.js** - Efectos de partículas animadas
- **Font Awesome** - Iconos
- **Google Fonts** - Tipografías (Poppins, Montserrat)

---

## 📡 Endpoints de la API

### GET `/`
Página principal de la interfaz web

### GET `/health`
Verificar estado del servidor
```json
{
  "status": "healthy",
  "timestamp": "2026-01-10T12:00:00",
  "chatbot_initialized": true
}
```

### POST `/chat`
Enviar mensaje al chatbot (HTTP)
```json
Request:
{
  "message": "¿Cuáles son las mejores atracciones?",
  "session_id": "optional_session_id"
}

Response:
{
  "response": "Las mejores atracciones son...",
  "timestamp": "2026-01-10T12:00:00",
  "session_id": "session_123"
}
```

### WebSocket `/ws/{session_id}`
Conexión WebSocket para chat en tiempo real
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/mi_sesion');

// Enviar mensaje
ws.send(JSON.stringify({ message: "Hola" }));

// Recibir respuesta
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data.content);
};
```

### GET `/attractions`
Obtener lista de atracciones
```json
{
  "count": 15,
  "attractions": [
    {
      "id": "laguna_paron",
      "name": "Laguna Parón",
      "description": "...",
      "altitude": 4185,
      "difficulty": "medio",
      "duration": "8-10 horas"
    }
  ]
}
```

### GET `/stats`
Obtener estadísticas de uso
```json
{
  "total_conversations": 42,
  "total_messages": 156,
  "active_connections": 3,
  "timestamp": "2026-01-10T12:00:00"
}
```

### GET `/history/{session_id}`
Obtener historial de conversación

### DELETE `/history/{session_id}`
Limpiar historial de conversación

---

## 🎨 Personalización

### Cambiar Colores

Edita las variables CSS en `static/css/style.css`:

```css
:root {
    --primary: #2563eb;
    --secondary: #10b981;
    --accent: #f59e0b;
    /* ... más colores */
}
```

### Cambiar Imágenes

Las imágenes de las atracciones se cargan desde Unsplash. Para usar imágenes locales:

1. Crea una carpeta `static/images/`
2. Guarda tus imágenes con nombres como `laguna_paron.jpg`
3. Actualiza `static/js/app.js`:

```javascript
<img src="/static/images/${attr.id}.jpg" alt="${attr.name}">
```

### Modificar Textos

Los textos principales están en `static/index.html`. Busca y reemplaza según necesites.

---

## 🐛 Solución de Problemas

### Error: "Cannot connect to WebSocket"

**Solución**: El WebSocket podría no estar disponible. La aplicación automáticamente usará HTTP como fallback.

### Error: "chatbot_instance is None"

**Solución**: 
1. Verifica que tu `OPENAI_API_KEY` esté configurada
2. Revisa los logs del servidor
3. Reinicia el servidor

### Las atracciones no se cargan

**Solución**:
1. Verifica que `data/knowledge/huaraz_knowledge.py` exista
2. Revisa la consola del navegador (F12)
3. Verifica el endpoint `/attractions` en `/docs`

### Partículas no se muestran

**Solución**: El CDN de particles.js podría estar bloqueado. Descarga la librería localmente.

---

## 📦 Despliegue en Producción

### Opción 1: Docker

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t huaraz-chatbot .
docker run -p 8000:8000 --env-file .env huaraz-chatbot
```

### Opción 2: Render / Railway / Fly.io

1. Sube tu código a GitHub
2. Conecta tu repositorio
3. Configura las variables de entorno
4. Despliega automáticamente

### Opción 3: VPS (DigitalOcean, AWS, etc.)

```bash
# Instalar en servidor
git clone tu_repositorio
cd chatbot_turismo_huaraz
pip install -r requirements.txt

# Usar un process manager
pip install gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# O con supervisor/systemd para mantener el proceso vivo
```

---

## 🔐 Seguridad

### Recomendaciones para Producción

1. **Usar HTTPS**: Configura SSL/TLS
2. **Limitar CORS**: Restringe orígenes permitidos
3. **Rate Limiting**: Implementa límites de peticiones
4. **Validación de Entrada**: Ya incluida con Pydantic
5. **Variables de Entorno**: Nunca commits API keys

### Ejemplo de Rate Limiting

```bash
pip install slowapi
```

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/chat")
@limiter.limit("10/minute")
async def chat(request: Request, message: ChatMessage):
    # ... código existente
```

---

## 📈 Monitoreo

### Logs

Los logs se imprimen en la consola. Para producción, considera:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Métricas

Considera integrar:
- **Prometheus** - Métricas de sistema
- **Grafana** - Visualización
- **Sentry** - Tracking de errores

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

## 👨‍💻 Soporte

- 📧 Email: soporte@huarazai.com
- 💬 Discord: [Tu servidor]
- 🐛 Issues: [GitHub Issues]

---

## 🎉 ¡Disfruta tu Chatbot!

Tu interfaz web moderna está lista. Explora Huaraz con inteligencia artificial. 🏔️✨
