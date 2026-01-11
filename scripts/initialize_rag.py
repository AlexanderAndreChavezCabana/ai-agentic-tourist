"""
Script para inicializar y probar el sistema RAG
"""
import os
import sys
from pathlib import Path

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.web_loader import HuarazWebRAG
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def initialize_rag_system(force_reload: bool = False):
    """
    Inicializar el sistema RAG.
    
    Args:
        force_reload: Forzar recarga de contenido web
    """
    # Cargar variables de entorno
    load_dotenv()
    
    logger.info("=" * 60)
    logger.info("INICIALIZANDO SISTEMA RAG PARA TURISMO HUARAZ")
    logger.info("=" * 60)
    
    # Verificar API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("❌ OPENAI_API_KEY no encontrada en .env")
        return False
    
    try:
        # Crear instancia RAG
        rag = HuarazWebRAG(openai_api_key=api_key)
        
        # Inicializar
        success = rag.initialize(force_reload=force_reload)
        
        if success:
            logger.info("✅ Sistema RAG inicializado exitosamente")
            
            # Hacer una búsqueda de prueba
            logger.info("\n" + "=" * 60)
            logger.info("PRUEBA DE BÚSQUEDA")
            logger.info("=" * 60)
            
            test_queries = [
                "precios de tours en huaraz",
                "hoteles en huaraz",
                "laguna 69 tour"
            ]
            
            for query in test_queries:
                logger.info(f"\n🔍 Búsqueda: '{query}'")
                results = rag.search(query, k=2)
                
                for i, doc in enumerate(results, 1):
                    source = doc.metadata.get('source', 'N/A')
                    preview = doc.page_content[:150].replace('\n', ' ')
                    logger.info(f"  {i}. [{source}]: {preview}...")
            
            logger.info("\n✅ Pruebas completadas")
            return True
        else:
            logger.error("❌ No se pudo inicializar el sistema RAG")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}", exc_info=True)
        return False


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Inicializar sistema RAG")
    parser.add_argument(
        '--force-reload',
        action='store_true',
        help='Forzar recarga de contenido web (ignorar caché)'
    )
    
    args = parser.parse_args()
    
    success = initialize_rag_system(force_reload=args.force_reload)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ Sistema RAG listo para usar")
        print("=" * 60)
        print("\nAhora puedes:")
        print("1. Ejecutar el chatbot: python app.py")
        print("2. El agente tendrá acceso a información web actualizada")
        print("3. Podrá responder sobre precios, tours y más")
        sys.exit(0)
    else:
        print("\n❌ Error al inicializar el sistema RAG")
        print("Revisa los logs arriba para más detalles")
        sys.exit(1)


if __name__ == "__main__":
    main()
