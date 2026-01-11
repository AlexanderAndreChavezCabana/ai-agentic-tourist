"""
Script para inicializar el scraper de precios
Extrae información estructurada de tours desde huarazturismo.com
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.price_scraper import HuarazPriceScraper
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Función principal"""
    print("=" * 70)
    print("🔍 SCRAPER DE PRECIOS - HUARAZ TURISMO")
    print("=" * 70)
    
    # Crear scraper
    scraper = HuarazPriceScraper()
    
    # Intentar cargar desde caché
    if scraper.load_from_cache():
        print(f"\n✅ Cargados {len(scraper.tours)} tours desde caché")
        
        response = input("\n¿Quieres actualizar los datos? (s/n): ")
        if response.lower() != 's':
            print_summary(scraper)
            return
    
    # Hacer scraping
    print("\n📥 Iniciando scraping de páginas web...")
    print(f"   Se procesarán {len(scraper.TOUR_PAGES)} páginas\n")
    
    tours = scraper.scrape_all_tours()
    
    if tours:
        print(f"\n✅ Scraping completado: {len(tours)} tours extraídos")
        
        # Guardar en caché
        scraper.save_to_cache()
        
        # Mostrar resumen
        print_summary(scraper)
    else:
        print("\n❌ No se pudo extraer información de tours")
        sys.exit(1)


def print_summary(scraper: HuarazPriceScraper):
    """Imprimir resumen de tours"""
    print("\n" + "=" * 70)
    print("📋 TOURS DISPONIBLES CON PRECIOS")
    print("=" * 70)
    
    for i, tour in enumerate(scraper.tours, 1):
        print(f"\n{i}. {tour.name}")
        if tour.price:
            print(f"   💰 Precio: {tour.price}")
        if tour.duration:
            print(f"   ⏱️  Duración: {tour.duration}")
        if tour.difficulty:
            print(f"   📊 Dificultad: {tour.difficulty}")
    
    print("\n" + "=" * 70)
    print("✅ Datos listos para usar en el chatbot")
    print("=" * 70)
    print("\nAhora puedes ejecutar: python app.py")
    print("\nPreguntas de ejemplo:")
    print("  - '¿Cuánto cuesta el tour a Laguna 69?'")
    print("  - 'Muéstrame todos los tours disponibles'")
    print("  - '¿Qué incluye el tour a Pastoruri?'\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping cancelado por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
