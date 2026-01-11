"""
Herramientas RAG para búsqueda web híbrida
"""
from typing import Dict, Any, Optional
from langchain_core.tools import tool
from src.rag.web_loader import HuarazWebRAG, format_search_results
from src.rag.price_scraper import get_scraper, HuarazPriceScraper
import logging

logger = logging.getLogger(__name__)

# Instancia global del sistema RAG
_rag_instance: Optional[HuarazWebRAG] = None


def get_rag_instance() -> HuarazWebRAG:
    """Obtener o crear instancia del sistema RAG"""
    global _rag_instance
    
    if _rag_instance is None:
        logger.info("Inicializando sistema RAG...")
        _rag_instance = HuarazWebRAG()
        
        # Intentar inicializar (usará caché si está disponible)
        if not _rag_instance.initialize(force_reload=False):
            logger.warning("No se pudo inicializar completamente el sistema RAG")
    
    return _rag_instance


@tool
def get_tour_price(tour_name: str) -> str:
    """
    Obtener información completa de un tour específico desde huarazturismo.com.
    Incluye precio actualizado, duración, qué incluye, y enlace clickeable para más detalles.
    
    Args:
        tour_name: Nombre del tour o destino (ej: "laguna 69", "pastoruri", "paquete 3d", "trekking santa cruz")
    
    Returns:
        Información detallada del tour con enlace clickeable para ver detalles completos
    """
    try:
        scraper = get_scraper()
        
        # Si no hay datos en caché, hacer scraping
        if not scraper.tours:
            logger.info("Realizando scraping de tours...")
            scraper.scrape_all_tours()
            scraper.save_to_cache()
        
        # Buscar el tour
        tour = scraper.get_tour_by_name(tour_name)
        
        if tour:
            formatted = scraper.format_tour_info(tour, include_html_link=True)
            
            # Si no tiene descripción completa, agregar nota
            if not tour.description or len(tour.description) < 50:
                formatted += "\n💡 **Tip**: Para más detalles específicos sobre este destino, pregúntame sobre características, altitud, mejor época para visitar, etc.\n"
            
            return formatted
        else:
            # Intentar búsqueda más amplia
            results = scraper.search_tours(tour_name)
            if results:
                formatted = scraper.format_tour_info(results[0], include_html_link=True)
                if len(results) > 1:
                    formatted += f"\n\n📌 También encontré {len(results)-1} tour(es) relacionado(s). ¿Quieres ver más opciones?\n"
                return formatted
            else:
                return f"No encontré información específica sobre '{tour_name}'.\n\n✅ Tours disponibles: laguna 69, pastoruri, llanganuco, chavin, paron, churup, santa cruz, entre otros.\n\n💡 Tip: Usa list_all_tours_with_prices() para ver todos los tours."
    
    except Exception as e:
        logger.error(f"Error obteniendo precio: {str(e)}")
        return f"Error al buscar información del tour. Por favor intenta con otro nombre o consulta la lista completa de tours."


@tool
def list_all_tours_with_prices() -> str:
    """
    Listar TODOS los tours, paquetes y trekking organizados por categoría.
    Muestra: Paquetes Turísticos (varios días), Tours Diarios (full day), y Trekking.
    Incluye precios y duraciones actualizadas.
    
    Returns:
        Lista completa categorizada con precios actualizados desde huarazturismo.com
    """
    try:
        scraper = get_scraper()
        
        # Si no hay datos, hacer scraping
        if not scraper.tours:
            logger.info("Realizando scraping de tours...")
            scraper.scrape_all_tours()
            scraper.save_to_cache()
        
        return scraper.get_all_tours_summary()
    
    except Exception as e:
        logger.error(f"Error listando tours: {str(e)}")
        return f"Error al obtener lista de tours: {str(e)}"


@tool
def search_web_tourism_info(query: str, max_results: int = 3) -> str:
    """
    Buscar información de turismo en páginas web externas de Huaraz.
    Útil para encontrar información general, descripciones y detalles actualizados.
    
    Args:
        query: Consulta de búsqueda (ej: "que visitar en huaraz", "mejor epoca")
        max_results: Número máximo de resultados a retornar
    
    Returns:
        Información relevante encontrada en páginas web
    """
    try:
        rag = get_rag_instance()
        
        if not rag.vector_store:
            return "⚠️ Sistema de búsqueda web no disponible temporalmente. Usando conocimiento base."
        
        # Buscar en el vector store
        results = rag.search(query, k=max_results)
        
        if not results:
            return f"No se encontró información web específica sobre: {query}"
        
        # Formatear resultados
        formatted = format_search_results(results)
        return formatted
        
    except Exception as e:
        logger.error(f"Error en búsqueda web: {str(e)}")
        return f"Error al buscar información web: {str(e)}"


@tool
def reload_web_content() -> str:
    """
    Recargar contenido web de páginas de turismo (admin tool).
    Actualiza la base de datos con información reciente.
    
    Returns:
        Mensaje de estado de la actualización
    """
    try:
        logger.info("Recargando contenido web...")
        rag = get_rag_instance()
        
        # Forzar recarga
        if rag.initialize(force_reload=True):
            return "✅ Contenido web actualizado exitosamente"
        else:
            return "⚠️ Hubo problemas al actualizar el contenido web"
            
    except Exception as e:
        logger.error(f"Error recargando contenido: {str(e)}")
        return f"❌ Error al recargar contenido: {str(e)}"
