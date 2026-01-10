# Chatbot Turístico Huaraz - IA Agéntica

Un asistente turístico inteligente especializado en Huaraz, Perú, construido con LangChain e IA agéntica. El sistema puede recomendar atracciones, crear itinerarios personalizados y responder preguntas específicas sobre turismo en la región.

## 🎯 Características Principales

### IA Agéntica
- **Agente Inteligente**: Sistema que puede razonar y tomar decisiones sobre qué herramientas usar
- **Herramientas Especializadas**: 7+ herramientas integradas para diferentes aspectos del turismo
- **Memoria Conversacional**: Mantiene contexto en conversaciones largas
- **Iteraciones Adaptativas**: El agente itera hasta encontrar la mejor respuesta

### Capacidades
- 📍 **Búsqueda de Atracciones**: Encuentra atracciones por tipo, dificultad y temporada
- 🗺️ **Creación de Itinerarios**: Genera planes diarios personalizados
- 🏨 **Recomendaciones de Alojamiento**: Sugiere hospedajes según presupuesto
- 🌤️ **Información de Clima**: Consejos sobre la mejor época para visitar
- 🏃 **Recomendaciones de Actividades**: Trekking, escalada, tours culturales, etc.
- ⚕️ **Consejos de Altitud**: Información sobre mal de altura y prevención
- 💬 **Conversación Natural**: Respuestas en español, contextuales y personalizadas

### Integraciones LLM
- OpenAI (GPT-4o, GPT-4 Turbo, GPT-3.5)
- Arquitectura extensible para otros proveedores

## 📁 Estructura del Proyecto

```
chatbot_turismo_huaraz/
├── config/
│   ├── model_config.yaml         # Configuración de modelos LLM
│   └── agent_config.yaml         # Configuración del agente
├── src/
│   ├── llm/
│   │   └── base.py               # Clientes para diferentes LLMs
│   ├── prompt_engineering/
│   │   └── prompts.py            # Gestión de prompts
│   ├── agents/
│   │   └── touristic_agent.py    # Agente turístico principal
│   ├── handlers/
│   │   └── tools.py              # Herramientas del agente
│   └── utils/
│       ├── config.py             # Cargador de configuraciones
│       └── helpers.py            # Utilidades generales
├── data/
│   └── knowledge/
│       └── huaraz_knowledge.py   # Base de conocimiento sobre Huaraz
├── examples/
│   ├── basic_usage.py            # Ejemplo de uso básico
│   ├── create_itinerary.py       # Creación de itinerarios
│   └── specialized_queries.py    # Consultas especializadas
├── notebooks/                     # Jupyter notebooks para experimentación
├── main.py                        # Aplicación principal
├── requirements.txt               # Dependencias
├── setup.py                       # Configuración del paquete
└── README.md                      # Esta documentación
```

## 🚀 Instalación

### Requisitos Previos
- Python 3.9+
- pip o conda
- API Keys para al menos un proveedor LLM

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
```bash
cd chatbot_turismo_huaraz
```

2. **Crear un entorno virtual** (recomendado)
```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
# Crear archivo .env en la raíz del proyecto
echo "OPENAI_API_KEY=tu_api_key_aqui" > .env
```

Ver [SETUP_OPENAI.md](SETUP_OPENAI.md) para instrucciones detalladas.

## 💬 Uso

### Modo Interactivo

```bash
python main.py
```

El chatbot iniciará una sesión interactiva donde puedes hacer preguntas sobre turismo en Huaraz.

Comandos especiales:
- `salir`: Terminar la conversación
- `preferencias`: Configurar tus preferencias (presupuesto, nivel de actividad, etc.)

### Uso Programático

```python
from main import ChatbotTouristico

# Crear instancia
chatbot = ChatbotTouristico(llm_provider="openai")

# Procesar consulta
response = chatbot.process_query("¿Cuál es la mejor atracción para principiantes?")
print(response)
```

### Ejemplos

```bash
# Ejemplo 1: Uso básico
python examples/basic_usage.py

# Ejemplo 2: Crear itinerario
python examples/create_itinerary.py

# Ejemplo 3: Consultas especializadas
python examples/specialized_queries.py
```

## 🛠️ Configuración

### Modelos LLM (config/model_config.yaml)

```yaml
models:
  openai:
    provider: "openai"
    model_name: "gpt-4-turbo"
    temperature: 0.7
    max_tokens: 2048
```

Puedes cambiar:
- `model_name`: Modelo específico a usar
- `temperature`: Creatividad (0.0-1.0)
- `max_tokens`: Longitud máxima de respuesta

### Configuración del Agente (config/agent_config.yaml)

```yaml
agent:
  name: "Guía Turístico Huaraz IA"
  max_iterations: 10
  max_execution_time: 60
```

## 🤖 Cómo Funciona la IA Agéntica

1. **Usuario hace una pregunta**
   ```
   "¿Qué actividades puedo hacer con mi familia en 2 días?"
   ```

2. **Agente analiza la consulta**
   - Identifica que necesita información de atracciones, actividades y posiblemente alojamiento
   - Determina el contexto (familia, 2 días)

3. **Agente selecciona herramientas**
   - Llama a `search_attractions`
   - Llama a `get_activity_recommendations`
   - Llama a `create_daily_itinerary`

4. **Agente procesa resultados**
   - Combina información
   - Personaliza según contexto
   - Genera respuesta coherente

5. **Respuesta al usuario**
   ```
   "Para tu familia, recomiendo la Laguna Llanganuco (bajo nivel de dificultad)
    combinada con un tour cultural. Aquí está el itinerario de 2 días..."
   ```

## 🔧 Herramientas Disponibles

1. **search_attractions**: Buscar atracciones por término o dificultad
2. **get_attraction_details**: Obtener información detallada de una atracción
3. **get_activity_recommendations**: Recomendar actividades
4. **search_accommodations**: Buscar alojamientos por presupuesto
5. **get_best_season**: Obtener mejor época según estilo de viaje
6. **get_altitude_advice**: Consejos para mal de altura
7. **create_daily_itinerary**: Crear itinerarios personalizados

## 📊 Datos de Huaraz

La base de conocimiento incluye:

### Atracciones
- Laguna Parón
- Laguna 69
- Nevado Pastoruri
- Laguna Llanganuco
- Chavín de Huántar

### Actividades
- Trekking en Cordillera Blanca
- Mountain Biking
- Escalada en Roca
- Tours Culturales

### Alojamientos
- Opciones presupuestarias (budget)
- Rango medio (mid_range)
- Lujo (luxury)

## 🔐 Seguridad

- Las API keys se cargan desde variables de entorno, nunca están en el código
- Usa un archivo `.env` y añádelo a `.gitignore`
- Valida todas las entradas del usuario

## 🤝 Personalización

### Añadir nuevas atracciones

En `data/knowledge/huaraz_knowledge.py`:

```python
@dataclass
class Attraction:
    name: str
    description: str
    location: str
    # ... más campos

# Añadir a ATTRACTIONS dictionary
```

### Crear nuevas herramientas

En `src/handlers/tools.py`:

```python
@tool
def nueva_herramienta(parametro: str) -> Dict[str, Any]:
    """Descripción de la herramienta"""
    # Implementación
    return resultado
```

Luego añádela a `TouristicAgent._setup_tools()`

## 📝 Ejemplos de Consultas

```
"¿Cuáles son las mejores atracciones para principiantes?"
"Quiero hacer trekking intenso, ¿qué me recomiendas?"
"Tengo 5 días y presupuesto bajo, crea un itinerario"
"¿Cuál es la mejor época para fotografía en Huaraz?"
"¿Cómo prepararse para el mal de altura?"
"¿Qué hay en Laguna 69?"
```

## 🐛 Solución de Problemas

### Error: "OPENAI_API_KEY not configured"
- Verifica que hayas creado el archivo `.env`
- Asegúrate de que la clave de API sea válida

### Error: "Proveedor no soportado"
- Usa uno de: `openai`, `anthropic`, `groq`
- Verifica la configuración en `config/model_config.yaml`

### Respuestas lentas
- Reduce `max_iterations` en `config/agent_config.yaml`
- Usa un modelo más rápido como Groq

## 📈 Mejoras Futuras

- [ ] Integración con base de datos vectorial (FAISS, Pinecone)
- [ ] Múltiples idiomas
- [ ] Integración con APIs reales (clima, precios de alojamiento)
- [ ] Interface web (Streamlit, Flask)
- [ ] Análisis de sentimientos
- [ ] Feedback y mejora continua

## 📄 Licencia

MIT License - Siéntete libre de usar este proyecto

## 👨‍💻 Autor

Desarrollado como un chatbot de turismo inteligente con IA agéntica

## 📞 Contacto

Para preguntas o sugerencias sobre mejoras, abre un issue en el repositorio.

---

**¡Disfruta explorando Huaraz con tu asistente de IA!** 🏔️
