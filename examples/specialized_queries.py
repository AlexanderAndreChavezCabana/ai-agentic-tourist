"""
Ejemplo 3: Consultas especializadas
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from main import ChatbotTouristico


def main():
    """Ejemplo de consultas especializadas"""
    
    print("="*60)
    print("EJEMPLO 3: CONSULTAS ESPECIALIZADAS".center(60))
    print("="*60)
    
    chatbot = ChatbotTouristico(llm_provider="openai")
    
    # Diferentes tipos de consultas
    queries = {
        "Actividades de aventura": "¿Qué actividades de trekking recomendadas hay en Huaraz?",
        "Altitud y salud": "Tengo miedo al mal de altura. ¿Qué debo hacer para prepararme?",
        "Mejor temporada": "¿Cuál es la mejor época para ir a Huaraz si quiero hacer fotografía de naturaleza?",
        "Rutas específicas": "Cuéntame detalladamente sobre la Laguna 69 - ubicación, dificultad, duración",
        "Presupuesto": "¿Cuál es el costo aproximado de un viaje de 3 días a Huaraz con presupuesto bajo?"
    }
    
    for title, query in queries.items():
        print(f"\n{'='*60}")
        print(f"CONSULTA: {title}")
        print(f"{'='*60}")
        print(f"P: {query}\n")
        
        response = chatbot.process_query(query)
        print(f"R: {response}")
        print()


if __name__ == "__main__":
    main()
