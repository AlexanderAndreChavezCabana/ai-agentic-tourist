"""
Agente Turístico con capacidades AgentIC y RAG
"""
from typing import Optional, List, Dict, Any
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, trim_messages
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from src.handlers.tools import (
    search_attractions,
    get_attraction_details,
    get_activity_recommendations,
    search_accommodations,
    get_best_season,
    get_altitude_advice,
    create_daily_itinerary
)
from src.handlers.rag_tools import (
    search_web_tourism_info,
    get_tour_price,
    list_all_tours_with_prices
)
from src.prompt_engineering.prompts import PromptManager


class TouristicAgent:
    """Agente turístico con capacidades agénticas"""
    
    def __init__(self, llm: Any, max_iterations: int = 10, memory_k: int = 10):
        """
        Inicializar el agente turístico.
        
        Args:
            llm: Modelo de lenguaje a utilizar
            max_iterations: Máximo número de iteraciones del agente
            memory_k: Número de mensajes a mantener en memoria (default: 10)
        """
        self.llm = llm
        self.max_iterations = max_iterations
        self.memory_k = memory_k
        self.tools = self._setup_tools()
        self.conversation_history: List[Dict[str, str]] = []
        self.user_context: Dict[str, Any] = {}
        # Sistema de memoria conversacional
        self.chat_history = InMemoryChatMessageHistory()
        self.agent_executor = self._create_agent_executor()
    
    def _setup_tools(self) -> List:
        """Configurar las herramientas disponibles para el agente"""
        return [
            # Herramientas locales
            search_attractions,
            get_attraction_details,
            get_activity_recommendations,
            search_accommodations,
            get_best_season,
            get_altitude_advice,
            create_daily_itinerary,
            # Herramientas RAG para búsqueda web
            search_web_tourism_info,
            # Herramientas de scraping de precios (más precisas)
            get_tour_price,
            list_all_tours_with_prices
        ]
    
    def _create_agent_executor(self) -> Any:
        """Crear el ejecutor del agente"""
        # Crear agente reactivo con herramientas
        # create_react_agent solo acepta model y tools como argumentos principales
        agent = create_react_agent(
            self.llm,
            self.tools
        )
        
        return agent
    
    def process_query(self, user_input: str) -> Dict[str, Any]:
        """
        Procesar una consulta del usuario.
        
        Args:
            user_input: Pregunta del usuario
        
        Returns:
            Respuesta del agente
        """
        try:
            # Agregar mensaje del usuario al historial
            self.chat_history.add_user_message(user_input)
            
            # Obtener mensajes del historial y limitar a los últimos K mensajes
            all_messages = self.chat_history.messages
            
            # Usar trim_messages para mantener solo los últimos K mensajes
            # Esto mantiene el contexto reciente sin sobrecargar el modelo
            trimmed_messages = trim_messages(
                all_messages,
                max_tokens=self.memory_k * 200,  # Aproximadamente K mensajes
                strategy="last",
                token_counter=len
            )
            
            # Agregar el mensaje actual
            messages_to_send = list(trimmed_messages) + [HumanMessage(content=user_input)]
            
            # Invocar el agente con el historial
            response = self.agent_executor.invoke({
                "messages": messages_to_send
            })
            
            # Extraer la respuesta del último mensaje
            output_text = ""
            if isinstance(response, dict) and "messages" in response:
                # Obtener el último mensaje que no sea del usuario
                messages = response["messages"]
                if messages:
                    last_message = messages[-1]
                    # Manejar diferentes formatos de contenido
                    if hasattr(last_message, 'content'):
                        content = last_message.content
                        # Si es una lista de dicts (formato de Google), extraer el texto
                        if isinstance(content, list) and len(content) > 0 and isinstance(content[0], dict):
                            output_text = content[0].get('text', str(content))
                        else:
                            output_text = str(content)
                    else:
                        output_text = str(last_message)
            elif isinstance(response, str):
                output_text = response
            else:
                output_text = str(response)
            
            # Guardar respuesta del asistente en memoria
            self.chat_history.add_ai_message(output_text)
            
            # Guardar en historial de conversación (mantener últimos 10)
            self.conversation_history.append({
                "user": user_input,
                "assistant": output_text
            })
            
            # Limitar historial a últimos 10 intercambios
            if len(self.conversation_history) > self.memory_k:
                self.conversation_history = self.conversation_history[-self.memory_k:]
            
            return {
                "success": True,
                "response": output_text,
                "tool_calls": []
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": "Disculpa, ocurrió un error procesando tu consulta. Por favor, intenta de nuevo."
            }
    
    def get_conversation_history(self) -> str:
        """Obtener historial de conversación formateado"""
        history_text = ""
        for exchange in self.conversation_history:
            history_text += f"Usuario: {exchange['user']}\nAsistente: {exchange['assistant']}\n\n"
        return history_text
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Obtener resumen del estado de la memoria"""
        return {
            "total_messages": len(self.chat_history.messages),
            "conversation_exchanges": len(self.conversation_history),
            "memory_limit": self.memory_k,
            "messages_in_history": [
                {"role": msg.type, "preview": str(msg.content)[:100]} 
                for msg in self.chat_history.messages[-5:]  # Últimos 5 mensajes
            ]
        }
    
    def clear_memory(self) -> None:
        """Limpiar completamente la memoria de conversación"""
        self.conversation_history = []
        self.chat_history.clear()
        self.user_context = {}
    
    def set_user_context(self, context: Dict[str, Any]) -> None:
        """
        Establecer contexto del usuario (preferencias, restricciones, etc.).
        
        Args:
            context: Diccionario con información del usuario
                    Ejemplo: {"budget": "mid_range", "fitness_level": "medio", "interests": ["nature", "culture"]}
        """
        self.user_context = context
        context_msg = f"Contexto del usuario: {context}"
        self.conversation_history.append({
            "user": "Información del usuario",
            "assistant": context_msg
        })


class AgentBuilder:
    """Constructor para crear agentes turísticos personalizados"""
    
    @staticmethod
    def create_agent(
        llm: Any,
        agent_type: str = "standard",
        max_iterations: int = 10
    ) -> TouristicAgent:
        """
        Crear un agente turístico personalizado.
        
        Args:
            llm: Modelo de lenguaje
            agent_type: Tipo de agente ("standard", "expert", "budget")
            max_iterations: Máximo de iteraciones
        
        Returns:
            Instancia del agente
        """
        agent = TouristicAgent(llm, max_iterations)
        
        if agent_type == "expert":
            # Para expertos: más iteraciones y herramientas avanzadas
            agent.max_iterations = 15
        elif agent_type == "budget":
            # Para presupuesto: enfoque en opciones económicas
            pass
        
        return agent
