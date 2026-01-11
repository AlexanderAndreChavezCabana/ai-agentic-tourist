"""
Scraper especializado para extraer precios y tours de huarazturismo.com
"""
import re
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import logging
from dataclasses import dataclass, asdict
import json
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class TourInfo:
    """Información estructurada de un tour"""
    name: str
    price: Optional[str] = None
    duration: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[str] = None
    includes: List[str] = None
    url: str = ""
    tour_type: str = "tour"  # "package", "tour", "trekking"
    
    def __post_init__(self):
        if self.includes is None:
            self.includes = []


class HuarazPriceScraper:
    """Scraper especializado para extraer precios de tours"""
    
    BASE_URL = "https://www.huarazturismo.com"
    
    # Paquetes Turísticos
    PACKAGE_PAGES = [
        "/paquete-huaraz-4d-3n.php",
        "/paquete-huaraz-3d-2n.php",
        "/paquete-huaraz-2d-1n.php",
        "/huaraz-de-aventura-2-dias-1-noche.php",
        "/paquete-turistico-huaraz-encantador-5d-4n.php",
        "/tour-huaraz-aventura-3d-2n.php",
        "/paquetes-turisticos-huaraz-3d-2n.php",
        "/paquete-huaraz-ideal-4d-3n.php",
    ]
    
    # Tours Diarios
    DAILY_TOUR_PAGES = [
        "/tours-laguna-llanganuco.php",
        "/tours-chavin-de-huantar.php",
        "/tours-nevado-pastoruri.php",
        "/tours-honcopampa.php",
        "/tours-huaraz.php",
        "/laguna-paron.php",
        "/tours-canon-del-pato.php",
        "/tours-chacas-punta-olimpica.php",
        "/tours-laguna-rocotuyoc-laguna-congelada.php",
    ]
    
    # Trekking
    TREKKING_PAGES = [
        "/trekking-laguna-69.php",
        "/trekking-santa-cruz-llanganuco.php",
        "/trekking-olleros-chavin.php",
        "/trekking-laguna-churup.php",
        "/trekking-quilcayhuanca-cojup.php",
        "/trekking-cedros-alpamayo.php",
        "/honda-ulta-trek.php",
        "/trekking-willcahuain-monterrey.php",
        "/laguna-wilcacocha-trek-huaraz.php",
    ]
    
    @property
    def TOUR_PAGES(self):
        """Combinar todas las páginas"""
        return self.PACKAGE_PAGES + self.DAILY_TOUR_PAGES + self.TREKKING_PAGES
    
    def __init__(self):
        self.tours: List[TourInfo] = []
        self.cache_file = Path("data/rag_cache/tours_data.json")
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
    
    def extract_price(self, soup: BeautifulSoup) -> Optional[str]:
        """Extraer precio de la página"""
        # Buscar patrones de precio
        price_patterns = [
            r'Precio:\s*S/\.?\s*(\d+)',
            r'S/\.?\s*(\d+)',
            r'Precio:\s*(\d+)',
        ]
        
        # Buscar en el texto completo
        text = soup.get_text()
        for pattern in price_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"S/ {match.group(1)}"
        
        # Buscar en elementos específicos
        price_elements = soup.find_all(['div', 'span'], class_=re.compile(r'precio|price|subtit'))
        for elem in price_elements:
            text = elem.get_text()
            match = re.search(r'S/\.?\s*(\d+)', text)
            if match:
                return f"S/ {match.group(1)}"
        
        return None
    
    def extract_duration(self, soup: BeautifulSoup) -> Optional[str]:
        """Extraer duración del tour"""
        text = soup.get_text()
        
        # Patrones de duración
        patterns = [
            r'Duración:\s*([^\n]+)',
            r'(\d+D/\d+N)',
            r'(Full\s+Day)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def extract_difficulty(self, soup: BeautifulSoup) -> Optional[str]:
        """Extraer nivel de dificultad"""
        text = soup.get_text()
        
        patterns = [
            r'Dificultad:\s*([^\n]+)',
            r'Nivel:\s*([^\n]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                difficulty = match.group(1).strip()
                # Limpiar
                difficulty = re.sub(r'\s+', ' ', difficulty)
                return difficulty[:50]  # Limitar longitud
        
        return None
    
    def extract_includes(self, soup: BeautifulSoup) -> List[str]:
        """Extraer lo que incluye el tour"""
        includes = []
        
        # Buscar sección "Incluye" o similar
        for header in soup.find_all(['h3', 'span', 'div', 'strong'], 
                                    string=re.compile(r'Incluye|Incluyen|Nuestros Precios Incluyen', re.IGNORECASE)):
            # Buscar la lista siguiente
            next_ul = header.find_next('ul')
            if next_ul:
                items = next_ul.find_all('li')
                includes.extend([item.get_text().strip() for item in items[:8]])  # Max 8 items
                break
        
        return includes
    
    def scrape_tour_page(self, url_path: str) -> Optional[TourInfo]:
        """Scrape una página de tour específica"""
        full_url = self.BASE_URL + url_path
        
        try:
            logger.info(f"Scraping: {full_url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(full_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraer título
            title = soup.find('title')
            name = title.get_text().split('|')[0].strip() if title else url_path
            
            # Limpiar nombre
            name = re.sub(r'\d{4}', '', name).strip()  # Remover años
            
            # Determinar tipo de tour
            tour_type = "tour"
            if "/paquete" in url_path or "/huaraz-" in url_path:
                tour_type = "package"
            elif "/trekking" in url_path or "/trek" in url_path:
                tour_type = "trekking"
            
            # Extraer información
            tour_info = TourInfo(
                name=name,
                price=self.extract_price(soup),
                duration=self.extract_duration(soup),
                difficulty=self.extract_difficulty(soup),
                includes=self.extract_includes(soup),
                url=full_url,
                tour_type=tour_type
            )
            
            # Extraer descripción (primeros párrafos)
            paragraphs = soup.find_all('p')[:3]
            description = ' '.join([p.get_text().strip() for p in paragraphs])
            tour_info.description = description[:300] if description else None
            
            logger.info(f"✓ Extraído: {name} ({tour_type}) - {tour_info.price or 'Sin precio'}")
            return tour_info
            
        except Exception as e:
            logger.error(f"Error scraping {full_url}: {str(e)}")
            return None
    
    def scrape_all_tours(self) -> List[TourInfo]:
        """Scrape todas las páginas de tours"""
        logger.info("Iniciando scraping de tours...")
        
        self.tours = []
        for url_path in self.TOUR_PAGES:
            tour = self.scrape_tour_page(url_path)
            if tour:
                self.tours.append(tour)
        
        logger.info(f"✓ Scraping completado: {len(self.tours)} tours encontrados")
        return self.tours
    
    def save_to_cache(self):
        """Guardar datos en caché"""
        try:
            data = [asdict(tour) for tour in self.tours]
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"✓ Datos guardados en: {self.cache_file}")
        except Exception as e:
            logger.error(f"Error guardando caché: {str(e)}")
    
    def load_from_cache(self) -> bool:
        """Cargar datos desde caché"""
        try:
            if not self.cache_file.exists():
                return False
            
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.tours = [TourInfo(**tour_data) for tour_data in data]
            logger.info(f"✓ Cargados {len(self.tours)} tours desde caché")
            return True
        except Exception as e:
            logger.error(f"Error cargando caché: {str(e)}")
            return False
    
    def search_tours(self, query: str) -> List[TourInfo]:
        """Buscar tours por nombre o descripción"""
        query_lower = query.lower()
        results = []
        
        for tour in self.tours:
            if (query_lower in tour.name.lower() or 
                (tour.description and query_lower in tour.description.lower())):
                results.append(tour)
        
        return results
    
    def get_tour_by_name(self, name: str) -> Optional[TourInfo]:
        """Obtener tour por nombre (búsqueda flexible)"""
        name_lower = name.lower()
        
        for tour in self.tours:
            if name_lower in tour.name.lower():
                return tour
        
        return None
    
    def format_tour_info(self, tour: TourInfo, include_html_link: bool = False) -> str:
        """Formatear información de tour para el usuario"""
        # Icono según tipo
        type_icons = {
            "package": "📦",
            "tour": "🎫", 
            "trekking": "🥾"
        }
        icon = type_icons.get(tour.tour_type, "🎫")
        
        text = f"{icon} **{tour.name}**\n\n"
        
        if tour.price:
            text += f"💰 **Precio**: {tour.price} por persona\n"
        else:
            text += f"💰 **Precio**: Consultar disponibilidad\n"
        
        if tour.duration:
            text += f"⏱️ **Duración**: {tour.duration}\n"
        
        if tour.difficulty:
            text += f"📊 **Dificultad**: {tour.difficulty}\n"
        
        if tour.description:
            text += f"\n📝 **Sobre el tour**: {tour.description}\n"
        
        if tour.includes and len(tour.includes) > 0:
            text += f"\n✅ **Incluye**:\n"
            for item in tour.includes[:8]:
                if item and len(item.strip()) > 3:
                    text += f"   • {item}\n"
        
        # Enlaces
        if include_html_link:
            # Para chat web con HTML
            text += f'\n<a href="{tour.url}" target="_blank" class="tour-link">📋 Ver detalles completos del tour</a>\n'
        else:
            # Para texto plano
            text += f"\n🔗 **Más información**: {tour.url}\n"
        
        text += f"\n📞 **Reservas**: WhatsApp +51 943833972 | Email: reservas@huarazviajes.com\n"
        
        return text
    
    def get_all_tours_summary(self) -> str:
        """Obtener resumen de todos los tours"""
        if not self.tours:
            return "No hay tours disponibles."
        
        # Agrupar por tipo
        packages = [t for t in self.tours if t.tour_type == "package"]
        daily_tours = [t for t in self.tours if t.tour_type == "tour"]
        trekking = [t for t in self.tours if t.tour_type == "trekking"]
        
        summary = "🎯 **TOURS Y PAQUETES DISPONIBLES EN HUARAZ**\n\n"
        
        if packages:
            summary += "**📦 PAQUETES TURÍSTICOS** (Varios días con alojamiento)\n\n"
            for tour in packages:
                price_str = tour.price if tour.price else "Consultar"
                duration_str = f" - {tour.duration}" if tour.duration else ""
                summary += f"   • **{tour.name}**: {price_str}{duration_str}\n"
            summary += "\n"
        
        if daily_tours:
            summary += "**🎫 TOURS DIARIOS** (Full Day)\n\n"
            for tour in daily_tours:
                price_str = tour.price if tour.price else "Consultar"
                duration_str = f" - {tour.duration}" if tour.duration else ""
                summary += f"   • **{tour.name}**: {price_str}{duration_str}\n"
            summary += "\n"
        
        if trekking:
            summary += "**🥾 TREKKING & CAMINATAS**\n\n"
            for tour in trekking:
                price_str = tour.price if tour.price else "Consultar"
                duration_str = f" - {tour.duration}" if tour.duration else ""
                summary += f"   • **{tour.name}**: {price_str}{duration_str}\n"
            summary += "\n"
        
        summary += "💡 **Tip**: Pregúntame por cualquier tour específico para ver detalles completos, qué incluye, y obtener el enlace directo.\n"
        
        return summary


# Instancia global
_scraper_instance: Optional[HuarazPriceScraper] = None


def get_scraper() -> HuarazPriceScraper:
    """Obtener instancia del scraper"""
    global _scraper_instance
    
    if _scraper_instance is None:
        _scraper_instance = HuarazPriceScraper()
        
        # Intentar cargar desde caché
        if not _scraper_instance.load_from_cache():
            logger.info("No hay caché, scraping necesario")
    
    return _scraper_instance
