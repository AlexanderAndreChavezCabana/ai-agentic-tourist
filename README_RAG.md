# 🌐 Sistema RAG - Búsqueda Web Híbrida

Sistema de **Retrieval-Augmented Generation (RAG)** que combina conocimiento local con información actualizada de páginas web de turismo en Huaraz.

## 🎯 ¿Qué hace?

El sistema RAG permite al chatbot:
- ✅ Buscar **precios actualizados** de tours y servicios
- ✅ Obtener información de **sitios web de turismo**
- ✅ Combinar conocimiento local + información web
- ✅ Responder con datos más precisos y actuales

## 🏗️ Arquitectura

```
┌─────────────────┐
│  Usuario hace   │
│  pregunta sobre │
│  precios/tours  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Agente Turístico               │
│  - Decide qué herramienta usar  │
│  - Combina múltiples fuentes    │
└────────┬───────────────┬────────┘
         │               │
         │               │
    ┌────▼────┐    ┌────▼─────────────┐
    │ Local   │    │  Sistema RAG     │
    │ Tools   │    │  (Web Search)    │
    └─────────┘    └──────┬───────────┘
                          │
                     ┌────▼────────┐
                     │ Vector DB   │
                     │ (FAISS)     │
                     │ + Embeddings│
                     └─────────────┘
```

## 📦 Componentes

### 1. **WebBaseLoader** (`src/rag/web_loader.py`)
- Carga contenido de páginas web
- Divide texto en chunks
- Crea embeddings con OpenAI
- Almacena en FAISS vector store

### 2. **Herramientas RAG** (`src/handlers/rag_tools.py`)
- `search_web_tourism_info`: Búsqueda general en web
- `search_prices_and_tours`: Búsqueda específica de precios

### 3. **Agente Integrado** (`src/agents/touristic_agent.py`)
- Combina herramientas locales + RAG
- Decide cuándo usar cada fuente
- Optimiza respuestas

## 🚀 Instalación

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno
Asegúrate de tener tu `OPENAI_API_KEY` en `.env`:
```env
OPENAI_API_KEY=sk-...
```

### 3. Inicializar el sistema RAG
```bash
python scripts/initialize_rag.py
```

**Opciones:**
- `--force-reload`: Forzar recarga de contenido web (ignora caché)

**Ejemplo:**
```bash
# Primera vez (carga contenido web)
python scripts/initialize_rag.py

# Actualizar contenido
python scripts/initialize_rag.py --force-reload
```

## 💻 Uso

### Desde el Chatbot Web
El sistema se integra automáticamente. Los usuarios pueden preguntar:

```
Usuario: "¿Cuánto cuesta el tour a la Laguna 69?"
Bot: [Usa search_prices_and_tours] → Responde con precios actualizados

Usuario: "Hoteles en Huaraz con precios"
Bot: [Usa search_web_tourism_info] → Busca en páginas web
```

### Desde Python
```python
from src.rag.web_loader import HuarazWebRAG

# Crear instancia
rag = HuarazWebRAG()

# Inicializar (carga desde caché si existe)
rag.initialize()

# Buscar información
results = rag.search("precio tour pastoruri", k=3)

for doc in results:
    print(doc.page_content)
    print(doc.metadata['source'])
```

## 🔧 Configuración

### URLs de Turismo
Edita en `src/rag/web_loader.py`:
```python
TOURISM_URLS = [
    "https://www.huarazturismo.com/",
    "https://www.huarazturismo.com/tours",
    # Añade más URLs aquí
]
```

### Parámetros de Búsqueda
```python
# En src/handlers/rag_tools.py
results = rag.search(query, k=3)  # k = número de resultados
```

## 📁 Estructura de Archivos

```
chatbot_turismo_huaraz/
├── src/
│   ├── rag/
│   │   ├── __init__.py
│   │   └── web_loader.py          # Sistema RAG principal
│   ├── handlers/
│   │   ├── tools.py               # Herramientas locales
│   │   └── rag_tools.py           # Herramientas web/RAG
│   └── agents/
│       └── touristic_agent.py     # Agente con RAG integrado
├── data/
│   └── rag_cache/                 # Caché del vector store
│       ├── faiss_index/           # Índice FAISS
│       └── vector_store.pkl       # Metadata
└── scripts/
    └── initialize_rag.py          # Script de inicialización
```

## 🎓 Cómo Funciona

### 1. Carga Inicial
```python
# Se ejecuta una vez
loader = WebBaseLoader(urls)
documents = loader.load()
```

### 2. Procesamiento
```python
# Divide en chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
chunks = splitter.split_documents(documents)

# Crea embeddings
embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_documents(chunks, embeddings)
```

### 3. Búsqueda
```python
# Usuario pregunta
query = "precio tour laguna 69"

# Busca chunks similares
results = vector_store.similarity_search(query, k=3)

# Retorna contexto relevante al agente
```

### 4. Caché
- Primera carga: Tarda ~1-2 minutos (depende de las URLs)
- Cargas posteriores: Instantáneas (usa caché)
- Actualización: `--force-reload` recarga todo

## ⚡ Optimización

### Reducir Tiempo de Carga
1. Reducir URLs en `TOURISM_URLS`
2. Ajustar `chunk_size` (menor = más chunks, más tiempo)
3. Usar caché (por defecto)

### Mejorar Calidad de Búsqueda
1. Aumentar `k` (más resultados)
2. Añadir más URLs relevantes
3. Ajustar `chunk_overlap` para mejor contexto

## 🐛 Troubleshooting

### Error: "Vector store no inicializado"
```bash
# Solución: Inicializar el sistema
python scripts/initialize_rag.py
```

### Error: "OPENAI_API_KEY no encontrada"
```bash
# Solución: Verificar .env
cat .env | grep OPENAI_API_KEY
```

### Búsquedas lentas
```python
# Solución: Verificar que usa caché
rag.load_vector_store()  # Debe retornar True
```

### Contenido desactualizado
```bash
# Solución: Forzar actualización
python scripts/initialize_rag.py --force-reload
```

## 📊 Métricas

El sistema registra:
- ✅ Número de documentos cargados
- ✅ Chunks creados
- ✅ Tiempo de inicialización
- ✅ Consultas realizadas

Ver logs en consola durante ejecución.

## 🔮 Próximas Mejoras

- [ ] Soporte para más sitios web
- [ ] Actualización automática periódica
- [ ] Filtros por tipo de contenido (precios, hoteles, tours)
- [ ] Integración con ChromaDB
- [ ] Búsqueda multimodal (imágenes)

## 📝 Notas

- **Costos**: Usa OpenAI Embeddings (~$0.0001 por 1K tokens)
- **Cache**: Almacenado en `data/rag_cache/`
- **Web Scraping**: Respeta términos de servicio de sitios web
- **Actualización**: Recomendado actualizar semanalmente

---

**Desarrollado para**: Chatbot Turístico Huaraz
**Tecnologías**: LangChain, FAISS, OpenAI Embeddings, BeautifulSoup
