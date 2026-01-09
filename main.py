"""
Aplicación Principal del Chatbot Turístico
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.llm.base import LLMFactory
from src.agents.touristic_agent import TouristicAgent, AgentBuilder
from src.utils.helpers import Logger, UserPreferences, EnvironmentConfig
from src.utils.config import ConfigLoader


class ChatbotTouristico:
    """Aplicación principal del chatbot turístico"""
    
    def __init__(self, llm_provider: str = "google"):
        """
        Inicializar el chatbot.
        
        Args:
            llm_provider: Proveedor de LLM a usar (google)
        """
        Logger.info("Inicializando Chatbot Turístico Huaraz...")
        
        # Cargar configuraciones
        self.config_loader = ConfigLoader(str(project_root / "config"))
        self.model_config = self.config_loader.load_model_config()
        self.agent_config = self.config_loader.load_agent_config()
        
        # Inicializar LLM
        Logger.info(f"Usando proveedor: {llm_provider}")
        model_settings = self.model_config.get("models", {}).get(llm_provider, {})
        
        self.llm = LLMFactory.get_model(
            llm_provider,
            **{k: v for k, v in model_settings.items() if k != "provider"}
        )
        
        # Crear agente
        self.agent = AgentBuilder.create_agent(
            self.llm,
            max_iterations=self.agent_config.get("agent", {}).get("max_iterations", 10)
        )
        
        # Preferencias del usuario
        self.user_preferences = UserPreferences()
        
        Logger.info("Chatbot inicializado exitosamente")
    
    def start_conversation(self) -> None:
        """Iniciar conversación interactiva con el usuario"""
        print("\n" + "="*60)
        print("CHATBOT TURÍSTICO - GUÍA DE HUARAZ".center(60))
        print("="*60)
        print("\nBienvenido al Asistente Turístico de Huaraz")
        print("Escribe tus preguntas sobre atracciones, actividades y viajes.")
        print("Escribe 'salir' para terminar la conversación.")
        print("Escribe 'preferencias' para configurar tus preferencias.")
        print("-"*60 + "\n")
        
        while True:
            try:
                user_input = input("Tú: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == "salir":
                    print("\n¡Gracias por usar el Chatbot Turístico! ¡Que disfrutes tu viaje a Huaraz!")
                    break
                
                if user_input.lower() == "preferencias":
                    self._show_preferences_menu()
                    continue
                
                # Procesar consulta
                Logger.info(f"Procesando consulta: {user_input}")
                response = self.agent.process_query(user_input)
                
                if response["success"]:
                    print(f"\nAsistente: {response['response']}\n")
                else:
                    print(f"\nAsistente: {response['response']}\n")
                    Logger.error(f"Error: {response.get('error', 'Error desconocido')}")
            
            except KeyboardInterrupt:
                print("\n\n¡Hasta luego!")
                break
            except Exception as e:
                Logger.error(f"Error en conversación: {str(e)}")
                print(f"\nAsistente: Disculpa, ocurrió un error. Por favor intenta de nuevo.\n")
    
    def _show_preferences_menu(self) -> None:
        """Mostrar menú de preferencias"""
        print("\n--- CONFIGURAR PREFERENCIAS ---")
        print("1. Presupuesto")
        print("2. Nivel de condición física")
        print("3. Intereses")
        print("4. Ver preferencias actuales")
        print("5. Volver")
        
        choice = input("\nSelecciona una opción (1-5): ").strip()
        
        if choice == "1":
            print("\nPresupuestos disponibles:")
            print("1. budget (económico)")
            print("2. mid_range (medio)")
            print("3. luxury (lujo)")
            budget = input("Selecciona tu presupuesto: ").strip().lower()
            if budget in ["budget", "mid_range", "luxury", "1", "2", "3"]:
                budget_map = {"1": "budget", "2": "mid_range", "3": "luxury"}
                budget = budget_map.get(budget, budget)
                self.user_preferences.set_preference("budget", budget)
                print(f"✓ Presupuesto actualizado a: {budget}")
        
        elif choice == "2":
            print("\nNiveles de condición:")
            print("1. bajo")
            print("2. medio")
            print("3. alto")
            level = input("Selecciona tu nivel: ").strip().lower()
            if level in ["bajo", "medio", "alto", "1", "2", "3"]:
                level_map = {"1": "bajo", "2": "medio", "3": "alto"}
                level = level_map.get(level, level)
                self.user_preferences.set_preference("fitness_level", level)
                print(f"✓ Nivel actualizado a: {level}")
        
        elif choice == "3":
            interests = input("Intereses (separados por coma, ej: naturaleza,cultura): ").strip().split(",")
            interests = [i.strip() for i in interests]
            self.user_preferences.set_preference("interests", interests)
            print(f"✓ Intereses actualizados: {', '.join(interests)}")
        
        elif choice == "4":
            prefs = self.user_preferences.get_all_preferences()
            print("\n--- TUS PREFERENCIAS ACTUALES ---")
            for key, value in prefs.items():
                print(f"  {key}: {value}")
        
        print()
    
    def process_query(self, user_input: str) -> str:
        """
        Procesar una consulta sin interfaz interactiva.
        
        Args:
            user_input: Pregunta del usuario
        
        Returns:
            Respuesta del agente
        """
        response = self.agent.process_query(user_input)
        return response["response"] if response["success"] else response.get("response", "Error")


def main():
    """Función principal"""
    try:
        # Crear instancia del chatbot
        chatbot = ChatbotTouristico(llm_provider="openai")
        
        # Iniciar conversación interactiva
        chatbot.start_conversation()
    
    except ValueError as e:
        Logger.error(f"Error de configuración: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        Logger.error(f"Error fatal: {str(e)}")
        print(f"Error fatal: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
