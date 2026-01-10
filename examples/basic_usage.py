"""
Ejemplo 1: Uso básico del chatbot
"""
import sys
from pathlib import Path

# Agregar raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import ChatbotTouristico


def main():
    """Ejemplo de uso básico"""
    
    print("="*60)
    print("EJEMPLO 1: USO BÁSICO DEL CHATBOT".center(60))
    print("="*60)
    
    # Crear instancia del chatbot
    chatbot = ChatbotTouristico(llm_provider="openai")
    
    # Ejemplos de consultas
    queries = [
        "¿Cuáles son las mejores atracciones turísticas en Huaraz?",
        "Quiero visitar Laguna Parón, ¿cuál es el mejor mes para ir?",
        "¿Qué actividades puedo hacer si tengo baja condición física?",
        "Dame recomendaciones de alojamiento con presupuesto bajo"
    ]
    
    print("\nProcesando consultas...\n")
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'='*60}")
        print(f"CONSULTA {i}: {query}")
        print(f"{'='*60}")
        
        response = chatbot.process_query(query)
        print(f"RESPUESTA:\n{response}")
        print()


if __name__ == "__main__":
    main()
