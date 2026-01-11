# 🎯 GUÍA RÁPIDA - Sistema RAG para Búsqueda Web

## 📋 Resumen
Has implementado con éxito un **sistema RAG (Retrieval-Augmented Generation)** que permite al chatbot buscar información actualizada en páginas web de turismo, especialmente **precios, tours y servicios**.

## 🚀 Instalación en 3 Pasos

### Paso 1: Instalar Dependencias
```bash
pip install -r requirements.txt
```

Esto instalará:
- `langchain-community` - Para WebBaseLoader
- `beautifulsoup4` & `lxml` - Para parsear HTML
- `faiss-cpu` - Vector database
- `tiktoken` - Tokenización

### Paso 2: Verificar Configuración
Asegúrate que tu `.env` tenga:
```env
OPENAI_API_KEY=sk-proj-...
```

### Paso 3: Inicializar Sistema RAG
```bash
python quickstart_rag.py
```

**¡Listo!** El sistema está configurado.

---

## 💻 Cómo Usar

### Opción A: Uso Automático (Recomendado)
Simplemente ejecuta tu chatbot normalmente:
```bash
python app.py
```

El agente **automáticamente** usará las herramientas RAG cuando:
- El usuario pregunte por precios
- Se necesite información actualizada
- Se mencionen tours o servicios

### Opción B: Actualizar Contenido Web
Para forzar actualización del contenido:
```bash
python scripts/initialize_rag.py --force-reload
```

---

## 🎓 Cómo Funciona

### 1. **El Usuario Pregunta**
```
Usuario: "¿Cuánto cuesta el tour a Pastoruri?"
```

### 2. **El Agente Decide**
```python
# El agente analiza y decide usar:
search_prices_and_tours("precio tour pastoruri")
```

### 3. **Sistema RAG Busca**
```python
# Busca en vector database (contenido de huarazturismo.com)
results = rag.search("precio tour pastoruri", k=3)
# Retorna: [documentos relevantes con precios]
```

### 4. **El Agente Responde**
```
Bot: "El tour al Nevado Pastoruri tiene un costo aproximado de...
     [información del sitio web]
     Fuente: www.huarazturismo.com"
```

---

## 🔧 Herramientas Disponibles

El agente ahora tiene estas herramientas **adicionales**:

### `search_prices_and_tours(query)`
**Cuándo usar:** Preguntas sobre precios, costos, tarifas
**Ejemplo:**
```python
query = "precio tour laguna 69"
# Retorna información de precios desde web
```

### `search_web_tourism_info(query)`
**Cuándo usar:** Información general actualizada
**Ejemplo:**
```python
query = "hoteles en huaraz"
# Retorna info de alojamiento desde web
```

---

## 📊 Ejemplos de Consultas

### Antes (solo conocimiento local):
```
Usuario: "¿Cuánto cuesta el tour a Laguna 69?"
Bot: "El costo estimado es entre $30-50 USD" ❌ (dato genérico)
```

### Después (con RAG):
```
Usuario: "¿Cuánto cuesta el tour a Laguna 69?"
Bot: [Usa search_prices_and_tours]
     "Según huarazturismo.com, el tour a Laguna 69 cuesta:
      - Tour compartido: S/. 80-100
      - Tour privado: S/. 300-400
      Incluye: transporte, guía, entrada al parque" ✅ (dato actualizado)
```

---

## 🎯 URLs Configuradas

Por defecto, el sistema carga de:
```python
TOURISM_URLS = [
    "https://www.huarazturismo.com/",
    "https://www.huarazturismo.com/tours",
    "https://www.huarazturismo.com/trekking",
    "https://www.huarazturismo.com/hoteles",
]
```

**Para añadir más URLs:**
1. Edita `src/rag/web_loader.py`
2. Añade URLs a `TOURISM_URLS`
3. Ejecuta: `python quickstart_rag.py`

---

## 🗂️ Archivos Creados

```
chatbot_turismo_huaraz/
├── src/
│   ├── rag/                          ← NUEVO
│   │   ├── __init__.py
│   │   └── web_loader.py            # Sistema RAG principal
│   └── handlers/
│       └── rag_tools.py             ← NUEVO: Herramientas web
├── data/
│   └── rag_cache/                   ← NUEVO: Caché del sistema
│       ├── faiss_index/
│       └── vector_store.pkl
├── scripts/
│   └── initialize_rag.py            ← NUEVO: Script inicialización
├── quickstart_rag.py                ← NUEVO: Setup rápido
├── README_RAG.md                    ← NUEVO: Documentación completa
└── requirements.txt                 ← ACTUALIZADO: Nuevas deps
```

---

## ⚙️ Configuración Avanzada

### Ajustar Número de Resultados
```python
# En src/handlers/rag_tools.py
results = rag.search(query, k=5)  # Default: 3
```

### Cambiar Tamaño de Chunks
```python
# En src/rag/web_loader.py
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,    # Default: 1000
    chunk_overlap=300   # Default: 200
)
```

### Caché
- **Ubicación:** `data/rag_cache/`
- **Borrar caché:** Elimina carpeta `data/rag_cache/`
- **Actualizar:** `python scripts/initialize_rag.py --force-reload`

---

## 🐛 Solución de Problemas

### ❌ "Vector store no inicializado"
```bash
python quickstart_rag.py
```

### ❌ "No module named 'faiss'"
```bash
pip install faiss-cpu
```

### ❌ "No se puede conectar a huarazturismo.com"
- Verifica tu conexión a internet
- El sistema usará conocimiento local como fallback

### ❌ Búsquedas muy lentas
- Primera vez: Normal (carga web ~1-2 min)
- Después: Instantáneo (usa caché)
- Si persiste: Reduce URLs en `TOURISM_URLS`

---

## 📈 Monitoreo

El sistema muestra logs en consola:
```
✅ Vector store cargado desde caché
🔍 Buscando: 'precio tour laguna 69'
✓ Encontrados 3 resultados
```

Para más detalle, configura logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 💡 Tips de Uso

1. **Primera ejecución:** Puede tardar 1-2 min cargando contenido web
2. **Ejecuciones posteriores:** Instantáneo (usa caché)
3. **Actualizar info:** Semanal o cuando cambien precios
4. **Combina fuentes:** El agente usa local + web automáticamente
5. **Precios precisos:** Siempre menciona fuente al usuario

---

## 📞 Soporte

Si tienes problemas:
1. Revisa logs en consola
2. Verifica `.env` tiene `OPENAI_API_KEY`
3. Ejecuta `python quickstart_rag.py` para diagnóstico
4. Consulta `README_RAG.md` para documentación completa

---

## ✅ Checklist de Implementación

- [x] Dependencias instaladas
- [x] Sistema RAG creado
- [x] Herramientas web añadidas al agente
- [x] Prompts actualizados
- [x] Scripts de inicialización
- [x] Documentación completa
- [x] Sistema de caché implementado

**Estado:** ✅ **LISTO PARA USAR**

---

## 🎉 ¡Felicidades!

Has implementado exitosamente un sistema RAG híbrido que combina:
- 🏠 Conocimiento local (rápido, siempre disponible)
- 🌐 Búsqueda web (actualizado, precios reales)
- 🤖 Agente inteligente (decide cuándo usar cada uno)

**Siguiente paso:** Ejecuta `python app.py` y prueba preguntando sobre precios!
