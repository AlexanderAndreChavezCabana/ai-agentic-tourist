# 🔍 Scraper de Precios - Guía Rápida

## ✨ Nuevo Sistema Implementado

He creado un **scraper especializado** que extrae precios y detalles estructurados directamente de huarazturismo.com.

## 🚀 Inicialización

### 1. Ejecutar el Scraper
```bash
python scripts/scrape_prices.py
```

Esto hará:
- ✅ Scraping de 12+ páginas de tours
- ✅ Extracción de precios, duración, dificultad
- ✅ Guardado en caché (data/rag_cache/tours_data.json)

**Primera vez:** Tarda ~30-60 segundos  
**Siguientes veces:** Instantáneo (usa caché)

### 2. Usar el Chatbot
```bash
python app.py
```

El sistema está **automáticamente integrado**.

## 💬 Ejemplos de Uso

### Preguntar por Precio Específico
```
Usuario: "¿Cuánto cuesta el tour a Laguna 69?"

Bot: [Usa get_tour_price("laguna 69")]
     
     **Caminata Laguna 69**
     
     💰 **Precio**: S/ 60
     ⏱️ **Duración**: Full Day
     📊 **Dificultad**: Moderado
     
     📝 **Descripción**: Visitaremos a Lagunas de Llanganuco...
     
     ✅ **Incluye**:
        • Transporte turístico
        • Guía profesional
        • Entrada al Parque Nacional
     
     🔗 **Más info**: https://www.huarazturismo.com/trekking-laguna-69.php
```

### Listar Todos los Tours
```
Usuario: "¿Qué tours hay disponibles?"

Bot: [Usa list_all_tours_with_prices()]
     
     📋 **Tours Disponibles en Huaraz:**
     
     • Laguna de Llanganuco - S/ 55 (Full Day)
     • Chavín de Huantar - S/ 55 (Full Day)
     • Nevado Pastoruri - S/ 55 (Full Day)
     • Caminata Laguna 69 - S/ 60 (Full Day)
     • Honcopampa - Chancos - S/ 55 (Full Day)
     • City Tours Huaraz - S/ 50 (04 hrs)
     ...
```

### Comparar Opciones
```
Usuario: "Quiero hacer trekking, ¿qué opciones tengo con precios?"

Bot: [Usa get_tour_price("trekking") + list_all_tours_with_prices()]
     
     Estas son las opciones de trekking disponibles:
     
     1. **Trekking Santa Cruz - Llanganuco** (5D/4N)
        💰 Sin precio específico en web (consultar)
        📊 Moderado a difícil
     
     2. **Laguna 69** (Full Day)
        💰 S/ 60
        📊 Moderado
     
     3. **Laguna Churup** (Full Day)
        💰 Consultar
        📊 Moderado
```

## 🔧 Herramientas del Agente

El chatbot ahora tiene estas herramientas:

### `get_tour_price(tour_name)`
**Uso:** Obtener precio y detalles de un tour específico  
**Ejemplo:** `get_tour_price("pastoruri")`  
**Retorna:** Precio, duración, dificultad, descripción, incluye

### `list_all_tours_with_prices()`
**Uso:** Listar todos los tours disponibles  
**Retorna:** Lista completa con precios y duraciones

### `search_web_tourism_info(query)`
**Uso:** Búsqueda general en contenido web  
**Ejemplo:** `search_web_tourism_info("mejor época para visitar")`

## 📊 Tours Scrapeados

El scraper extrae información de:

1. ✅ Laguna de Llanganuco (S/ 55)
2. ✅ Chavín de Huantar (S/ 55)
3. ✅ Nevado Pastoruri (S/ 55)
4. ✅ Laguna 69 (S/ 60)
5. ✅ Honcopampa - Chancos (S/ 55)
6. ✅ City Tours Huaraz (S/ 50)
7. ✅ Laguna Parón (consultar)
8. ✅ Cañón del Pato (S/ 90)
9. ✅ Chacas - Punta Olímpica (S/ 70)
10. ✅ Trekking Santa Cruz - Llanganuco (5D/4N)
11. ✅ Trekking Olleros - Chavín
12. ✅ Trekking Laguna Churup

## 🔄 Actualizar Datos

Para actualizar precios desde la web:

```bash
python scripts/scrape_prices.py
```

Cuando pregunte "¿Quieres actualizar los datos?", responde `s` (sí).

**Frecuencia recomendada:** Semanal o cuando cambien precios

## 📁 Archivos Creados

```
src/
├── rag/
│   ├── price_scraper.py          # Scraper especializado
│   └── web_loader.py             # Sistema RAG original
└── handlers/
    └── rag_tools.py              # Herramientas actualizadas

scripts/
└── scrape_prices.py              # Script de inicialización

data/
└── rag_cache/
    ├── tours_data.json           # Datos extraídos (caché)
    └── faiss_index/              # Vector store
```

## 💡 Ventajas del Nuevo Sistema

### Antes (Solo RAG):
- ❌ Búsqueda semántica general
- ❌ Precios mezclados con texto
- ❌ Difícil extraer datos precisos

### Ahora (Scraper + RAG):
- ✅ Extracción estructurada de datos
- ✅ Precios precisos y actualizados
- ✅ Información organizada (precio, duración, incluye)
- ✅ Búsqueda por nombre exacto
- ✅ Caché para rapidez

## 🎯 Flujo de Trabajo

```
Usuario pregunta por precio
         ↓
Agente decide usar get_tour_price()
         ↓
Scraper busca en caché
         ↓
Si no hay caché → Scrapea web
         ↓
Extrae: nombre, precio, duración, incluye
         ↓
Formatea respuesta
         ↓
Usuario recibe info estructurada
```

## 🐛 Troubleshooting

### "No se encontró información sobre X"
- Ejecuta: `python scripts/scrape_prices.py`
- El scraper actualizará los datos

### Scraper lento
- Normal la primera vez (~1 min)
- Usa caché después (instantáneo)

### Precios desactualizados
- Ejecuta scraper con actualización: `python scripts/scrape_prices.py` → `s`

## ✅ Prueba Ahora

```bash
# 1. Inicializar scraper
python scripts/scrape_prices.py

# 2. Ejecutar chatbot
python app.py

# 3. Preguntar:
"¿Cuánto cuesta el tour a Laguna 69?"
"Muéstrame todos los tours disponibles"
"¿Qué incluye el tour a Pastoruri?"
```

---

**Estado:** ✅ **IMPLEMENTADO Y LISTO**

El scraper extrae automáticamente:
- 💰 Precios (S/.)
- ⏱️ Duración (Full Day, 5D/4N, etc.)
- 📊 Dificultad (Moderado, Difícil, etc.)
- 📝 Descripción
- ✅ Qué incluye
- 🔗 URL de la fuente
