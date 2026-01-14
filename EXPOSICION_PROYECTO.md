# Exposición del Proyecto: Chatbot Turístico Huaraz AI
**Alexander Chavez**

## Planteamiento del Problema

El turismo en Huaraz, uno de los principales destinos de aventura y naturaleza en Perú, enfrenta varios retos en la atención y orientación a turistas nacionales y extranjeros:

- La información sobre tours, precios, clima y recomendaciones suele estar dispersa, desactualizada o solo disponible en horarios limitados.
- Las agencias y operadores turísticos dedican mucho tiempo a responder preguntas frecuentes y personalizar itinerarios, lo que reduce su eficiencia.
- Los turistas requieren respuestas inmediatas, confiables y personalizadas para planificar mejor su viaje y aprovechar al máximo su estadía.
- La falta de integración de datos en tiempo real (precios, clima, disponibilidad) dificulta la toma de decisiones informadas.

**Justificación:**
Un asistente virtual inteligente, capaz de integrar información actualizada de múltiples fuentes, responder en lenguaje natural y personalizar recomendaciones, puede transformar la experiencia turística en Huaraz. Automatiza la atención, reduce la carga operativa de las agencias y mejora la satisfacción del visitante, aportando innovación tecnológica al sector turístico local.


## 1. Resumen General

**Chatbot Turístico Huaraz AI** es un asistente virtual inteligente especializado en turismo en la Cordillera Blanca (Huaraz, Perú). Utiliza IA generativa, RAG (Retrieval-Augmented Generation), scraping web en tiempo real, memoria conversacional y agentes inteligentes para brindar información actualizada sobre tours, clima, itinerarios y recomendaciones personalizadas. Cuenta con una interfaz web moderna y responsive.

## 2. Objetivos del Proyecto
- Brindar información turística actualizada y personalizada.
- Automatizar la atención a turistas y agencias.
- Integrar fuentes de datos en tiempo real (precios, clima, tours).
- Ofrecer recomendaciones e itinerarios personalizados.

## 3. Arquitectura y Componentes

### Backend
- **FastAPI**: Framework web asíncrono.
- **LangChain & LangGraph**: Orquestación de modelos de lenguaje y agentes.
- **OpenAI GPT-4o-mini**: Modelo de lenguaje principal.
- **BeautifulSoup4**: Web scraping de tours.
- **FAISS**: Vector store para búsqueda semántica.

### Frontend
- **HTML5, CSS3, JavaScript (Vanilla)**
- **Particles.js**: Efectos visuales.
- **WebSocket API**: Comunicación en tiempo real.

### APIs Externas
- **OpenAI API**
- **OpenWeatherMap API**
- **huarazturismo.com** (scraping)

## 4. Principales Módulos y Estructura

- `src/agents/`: Agentes inteligentes (LangGraph, memoria)
- `src/handlers/`: Herramientas del agente y RAG
- `src/llm/`: Configuración de LLM (OpenAI)
- `src/prompt_engineering/`: Prompts optimizados
- `src/rag/`: Sistema RAG, scraping y vector store
- `src/utils/`: Utilidades y configuración
- `data/`: Datos, cache y base de conocimiento
- `static/`: Interfaz web (HTML, CSS, JS)
- `scripts/`: Scraping y setup de datos
- `config/`: Configuración YAML del agente y modelo
- `examples/`: Ejemplos de uso
- `notebooks/`: Experimentación Jupyter

## 5. Instalación y Ejecución

### Prerrequisitos
- Python 3.10+
- pip
- Git
- Cuenta OpenAI (API key)

### Pasos
1. Clonar el repositorio
2. Crear entorno virtual y activar
3. Instalar dependencias: `pip install -r requirements.txt`
4. Configurar `.env` con las API keys
5. Ejecutar scraping: `python scripts/scrape_prices.py`
6. Inicializar RAG: `python quickstart_rag.py`
7. Iniciar servidor: `python app.py`
8. Acceder a `http://localhost:8000`

## 6. Funcionalidades Clave
- Búsqueda de tours y precios actualizados (scraping + cache)
- Consulta de clima en tiempo real (OpenWeatherMap)
- Memoria conversacional (contexto de usuario)
- Creación de itinerarios personalizados
- 12 herramientas especializadas para el agente
- Interfaz web moderna y responsive

## 7. Ejemplo de Uso
- "¿Cuánto cuesta el tour a Laguna 69?"
- "¿Cómo está el clima en Huaraz?"
- "Crea un itinerario de 3 días para nivel intermedio"

## 8. Despliegue
- Docker y Docker Compose listos para producción
- Variables de entorno para configuración avanzada

## 9. Testing
- Tests automáticos: `python test_chatbot.py`, `python test_imports.py`
- Ejemplos programáticos en `examples/`

## 10. Recursos y Documentación
- [TECHNICAL.md](TECHNICAL.md): Arquitectura técnica
- [SETUP_RAG.md](SETUP_RAG.md): Guía RAG
- [SCRAPER_GUIDE.md](SCRAPER_GUIDE.md): Scraper
- [QUICKSTART.md](QUICKSTART.md): Inicio rápido

## 11. Métricas del Proyecto
- ~8,500 líneas de código
- 25+ archivos Python
- 12 herramientas del agente
- 26+ tours en base de datos
- <2s tiempo de respuesta promedio

## 12. Roadmap
- Multiidioma, reservas online, chatbot por voz, app móvil, integración WhatsApp, dashboard analytics, AR para tours virtuales.



---

_Última actualización: Enero 2026_
## 14. ¿Cómo funciona la IA y LangChain en el proyecto?

### Arquitectura y Flujo de Proceso de IA

1. **Recepción de la consulta**: El usuario envía una pregunta (por web, API o CLI). El sistema valida la entrada y carga el contexto de memoria (historial de conversación).

2. **Análisis y planificación**: El agente principal (TouristicAgent) analiza la consulta y decide qué herramientas usar (por ejemplo, buscar tours, consultar clima, crear itinerario, etc.). Utiliza el patrón de agentes de LangChain (Agent Executor) para planificar y ejecutar iteraciones.

3. **Ejecución de herramientas**: El agente ejecuta las herramientas necesarias, como scraping de precios, consulta de clima, búsqueda en la base de conocimiento, etc. Cada herramienta es una función especializada decorada con `@tool` de LangChain.

4. **Generación de respuesta**: El modelo LLM (GPT-4o-mini u otro) genera una respuesta personalizada usando prompts optimizados y el contexto del usuario. Se incorporan resultados de las herramientas y memoria conversacional.

5. **Entrega y almacenamiento**: El chatbot devuelve la respuesta al usuario, guarda la interacción en la memoria conversacional y formatea la salida para legibilidad.

### Componentes Clave de IA

- **LLM Factory**: Permite usar diferentes proveedores de modelos (OpenAI, Anthropic, Groq) de forma intercambiable.
- **TouristicAgent**: Orquesta la lógica, decide qué herramientas usar, mantiene el historial y maneja errores.
- **Herramientas (Tools)**: Funciones especializadas para buscar atracciones, obtener detalles, recomendar actividades, crear itinerarios, etc.
- **Prompt Engineering**: Prompts optimizados para cada tipo de consulta, con ejemplos y contexto.
- **Memoria Conversacional**: Se usa `ConversationBufferMemory` para recordar los últimos mensajes y mantener coherencia en la conversación.
- **Knowledge Base**: Base de datos local de atracciones, actividades y alojamientos, consultada por las herramientas.

### Ejemplo de Flujo de Consulta

1. Usuario: "¿Cuánto cuesta el tour a Laguna 69?"
2. El agente identifica que debe usar la herramienta de scraping de precios.
3. Ejecuta la función `get_tour_price()` y obtiene el precio actualizado.
4. El LLM genera una respuesta clara y personalizada, integrando el precio y detalles del tour.
5. La respuesta se entrega al usuario y se guarda en la memoria para futuras referencias.

### Iteraciones y Razonamiento del Agente

El agente puede realizar varias iteraciones (máximo configurable) para resolver consultas complejas, usando diferentes herramientas y refinando la respuesta antes de entregarla.

### Extensibilidad y Personalización

- Se pueden agregar nuevas herramientas fácilmente.
- La configuración del agente y el modelo es editable vía YAML.
- La base de conocimiento es ampliable.

---

Esta sección explica el proceso completo de IA, el rol de LangChain y cómo se orquesta la inteligencia artificial en el proyecto.

---

## 15. ¿Dónde está el RAG y cómo funciona el vector store?

### ¿Qué es RAG en este proyecto?
RAG (Retrieval-Augmented Generation) es la técnica que permite al chatbot buscar información relevante en fuentes externas (web, base de datos, scraping) y combinarla con la generación de texto del modelo LLM. Así, el asistente puede responder con datos actualizados y precisos.

### Componentes RAG en el proyecto
- **Scraping de tours y precios**: El archivo `src/rag/price_scraper.py` extrae y estructura información de tours, precios, duración, dificultad, etc., desde huarazturismo.com. Los datos se guardan en `data/rag_cache/tours_data.json`.
- **Carga y vectorización de contenido web**: El archivo `src/rag/web_loader.py` usa `WebBaseLoader` para cargar contenido de páginas web turísticas y lo divide en fragmentos (chunks) usando `RecursiveCharacterTextSplitter`.
- **Embeddings y vector store**: Se generan embeddings (vectores numéricos) de los fragmentos usando `OpenAIEmbeddings`. Estos vectores se almacenan en un índice FAISS (`data/rag_cache/faiss_index/`).
- **Búsqueda semántica**: Cuando el usuario hace una consulta, el sistema busca los fragmentos más relevantes en el vector store usando similitud de embeddings.
- **Integración con el LLM**: Los resultados relevantes se pasan al modelo LLM, que los utiliza para generar una respuesta informada y contextualizada.

### Flujo resumido del sistema RAG
1. **Scraping**: Se ejecuta `python scripts/scrape_prices.py` para extraer y guardar datos de tours.
2. **Inicialización RAG**: Se ejecuta `python quickstart_rag.py` para cargar contenido web, crear el vector store y guardar el índice FAISS.
3. **Consulta**: Cuando el usuario pregunta, el agente usa el vector store para buscar información relevante y la integra en la respuesta.

### ¿Dónde se pone el vector?
- El vector store (índice FAISS) se guarda en `data/rag_cache/faiss_index/`.
- El código para crear, guardar y cargar el vector store está en `src/rag/web_loader.py` (métodos `create_vector_store`, `save_vector_store`, `load_vector_store`).
- El scraping de tours y su cache está en `data/rag_cache/tours_data.json`.

### Ejemplo de uso en código
```python
from src.rag.web_loader import HuarazWebRAG
rag = HuarazWebRAG()
rag.initialize()  # Carga o crea el vector store
resultados = rag.search("Laguna 69", k=3)  # Busca fragmentos relevantes
```

---

Esta sección explica claramente cómo se implementa RAG, dónde se almacena el vector store y cómo se integra la búsqueda semántica en el flujo de IA del chatbot.

---

## 16. ¿Cómo se recupera la información desde el vector store?

### Proceso de recuperación paso a paso
1. **El usuario realiza una consulta** (por ejemplo: "¿Qué actividades hay en Laguna 69?").
2. **El agente detecta que necesita información externa** y utiliza el sistema RAG.
3. **La consulta se convierte en un embedding** (vector numérico) usando el mismo modelo de embeddings que se usó para indexar los documentos (OpenAIEmbeddings).
4. **Se realiza una búsqueda de similitud** en el índice FAISS:
   - El vector de la consulta se compara con todos los vectores almacenados.
   - Se seleccionan los fragmentos (chunks) de texto más similares (por ejemplo, los 3 o 4 más relevantes).
5. **Se recuperan los textos originales** asociados a esos vectores (incluyendo metadatos como la fuente web).
6. **El agente pasa estos textos al modelo LLM** como contexto adicional en el prompt.
7. **El LLM genera una respuesta** que integra la información recuperada y la presenta al usuario de forma natural.

### Ejemplo de código de recuperación
```python
from src.rag.web_loader import HuarazWebRAG
rag = HuarazWebRAG()
rag.initialize()  # Carga el vector store
resultados = rag.search("Laguna 69", k=3)  # Recupera los 3 fragmentos más relevantes
for doc in resultados:
	print(doc.page_content)  # Texto relevante recuperado
```

### Detalle de la función de búsqueda
- El método `search(query, k)` convierte la consulta en embedding y usa `self.vector_store.similarity_search(query, k=k)` para obtener los fragmentos más similares.
- Cada fragmento es un objeto `Document` que contiene el texto y metadatos (fuente, tipo, etc.).
- El agente puede formatear estos resultados y pasarlos al LLM para enriquecer la respuesta.

### ¿Qué ventajas tiene este enfoque?
- Permite responder con información actualizada y específica, incluso si el LLM no la conocía previamente.
- Hace posible que el chatbot cite fuentes y brinde respuestas más confiables.

---
