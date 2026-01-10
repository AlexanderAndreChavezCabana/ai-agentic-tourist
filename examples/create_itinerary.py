"""
Ejemplo 2: Crear un itinerario personalizado
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from main import ChatbotTouristico
from src.utils.helpers import UserPreferences


def main():
    """Ejemplo de creación de itinerario personalizado"""
    
    print("="*60)
    print("EJEMPLO 2: ITINERARIO PERSONALIZADO".center(60))
    print("="*60)
    
    chatbot = ChatbotTouristico(llm_provider="openai")
    
    # Configurar preferencias del usuario
    print("\nConfigurando preferencias del usuario...")
    prefs = {
        "budget": "mid_range",
        "fitness_level": "medio",
        "interests": ["naturaleza", "fotografía"],
        "duration_days": 5
    }
    chatbot.user_preferences.update_preferences(prefs)
    
    print(f"Preferencias configuradas:")
    for key, value in prefs.items():
        print(f"  - {key}: {value}")
    
    # Consultar para itinerario
    query = """
    Soy visitante de Huaraz con 5 días disponibles. 
    Tengo presupuesto medio, nivel de condición física medio, 
    y me interesan la naturaleza y la fotografía.
    Crea un itinerario detallado por días incluyendo:
    - Atracciones recomendadas
    - Horarios
    - Qué llevar
    - Costo estimado
    - Consejos importantes
    """
    
    print("\n" + "="*60)
    print("CREANDO ITINERARIO DE 5 DÍAS")
    print("="*60 + "\n")
    
    response = chatbot.process_query(query)
    print(response)


if __name__ == "__main__":
    main()
