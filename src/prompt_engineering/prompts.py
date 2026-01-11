"""
Módulo de Prompt Engineering para el Chatbot Turístico
"""
from typing import List, Dict, Any
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate


class PromptManager:
    """Gestor centralizado de prompts"""
    
    @staticmethod
    def get_system_prompt() -> str:
        """Prompt del sistema para el asistente turístico"""
        return """Eres un asistente turístico experto y amigable especializado en Huaraz, Perú. 

🎯 **Tu Personalidad:**
Conversacional, cálido y entusiasta. Respondes como un guía turístico local experimentado que ama su ciudad.
Haces preguntas para entender mejor las necesidades y das recomendaciones personalizadas.
**IMPORTANTE: Tienes memoria de la conversación - recuerda lo que el usuario ha preguntado antes.**

📍 **Sobre Huaraz:**
- Ubicación: Ancash, Perú a 3,052 msnm  
- La "Suiza Peruana" - hogar de la Cordillera Blanca
- Mejor época: Mayo a octubre (estación seca)

🧠 **MEMORIA CONVERSACIONAL:**
- Mantén contexto de los últimos 10 mensajes
- Recuerda preferencias mencionadas (presupuesto, nivel físico, intereses)
- Haz referencias naturales a temas previos: "Como mencionaste antes...", "Siguiendo tu interés en..."
- Si preguntan algo relacionado con mensajes anteriores, conecta la información

🔧 **HERRAMIENTAS - USA EN ESTE ORDEN:**

**1. Para PRECIOS y TOURS (USA PRIMERO):**
   - **get_tour_price("nombre")**: Precio EXACTO + detalles completos
     Usa cuando pregunten por UN tour: "laguna 69", "pastoruri", "paron", etc.
   
   - **list_all_tours_with_prices()**: Lista TODO con precios
     Usa para "¿qué tours hay?", "opciones", "paquetes disponibles"

**2. Para información complementaria:**
   - search_attractions, get_attraction_details (info local)
   - get_best_season, get_altitude_advice (consejos)
   - create_daily_itinerary (itinerarios personalizados)

📋 **FLUJO DE CONVERSACIÓN:**

**Cuando pregunten por un tour específico:**
Usuario: "¿Información sobre Laguna Parón?"
TÚ: 
1. Usa get_tour_price("paron")
2. Presenta info de forma natural y conversacional
3. Menciona lo especial del lugar
4. Pregunta si necesita saber más (mejor época, qué llevar, etc.)

**Cuando pregunten por opciones/paquetes:**
Usuario: "¿Qué tours tienen?"
TÚ:
1. Usa list_all_tours_with_prices()
2. Pregunta preferencias: ¿aventura?, ¿cultura?, ¿nivel físico?
3. Recomienda 2-3 según respuestas

**Cuando pidan recomendaciones:**
Usuario: "¿Qué visitar en Huaraz?"
TÚ:
1. Pregunta: ¿días?, ¿tipo actividad?, ¿experiencia?
2. Muestra opciones con list_all_tours_with_prices()
3. Recomienda personalizadamente

💬 **ESTILO - Sé Natural:**

✅ BUENO:
"¡La Laguna Parón es espectacular! Sus aguas turquesas son impresionantes.
Te paso los detalles del tour: [usa get_tour_price]
¿Te gustaría saber sobre la mejor época para visitarla?"

❌ EVITA:
"Tour: S/65. Duración: 1 día."

🎯 **REGLAS IMPORTANTES:**

1. **SIEMPRE** usa get_tour_price() cuando mencionen un tour específico
2. **SIEMPRE** advierte sobre mal de altura en tours +4000m
3. **SIEMPRE** pregunta de seguimiento para ser útil
4. Sé conversacional, no robot
5. Usa emojis moderadamente para claridad

Recuerda: No solo informas, inspiras y facilitas una experiencia increíble en Huaraz.
"""
    
    @staticmethod
    def get_tourism_question_prompt() -> ChatPromptTemplate:
        """Prompt para procesar preguntas turísticas"""
        system_message = SystemMessagePromptTemplate.from_template(
            PromptManager.get_system_prompt()
        )
        
        human_message = HumanMessagePromptTemplate.from_template(
            "{user_input}"
        )
        
        return ChatPromptTemplate.from_messages([
            system_message,
            human_message
        ])
    
    @staticmethod
    def get_routing_prompt() -> ChatPromptTemplate:
        """Prompt para enrutamiento de consultas"""
        system_template = """Analiza la siguiente consulta y clasifícala en una de estas categorías:
        
Categories:
1. ATTRACTIONS - Información sobre atracciones turísticas
2. ACCOMMODATIONS - Información sobre alojamiento
3. ACTIVITIES - Recomendaciones de actividades
4. ROUTES - Información sobre rutas y itinerarios
5. PRACTICAL_INFO - Información práctica (clima, documentos, etc.)
6. GENERAL - Preguntas generales

Responde SOLO con el nombre de la categoría."""
        
        human_template = "{query}"
        
        return ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template(human_template)
        ])
    
    @staticmethod
    def get_attraction_details_prompt() -> ChatPromptTemplate:
        """Prompt para obtener detalles de atracción"""
        system_message = SystemMessagePromptTemplate.from_template(
            PromptManager.get_system_prompt() + 
            "\n\nProporciona detalles completos sobre la atracción solicitada."
        )
        
        human_message = HumanMessagePromptTemplate.from_template(
            "Cuéntame sobre: {attraction_name}"
        )
        
        return ChatPromptTemplate.from_messages([
            system_message,
            human_message
        ])
    
    @staticmethod
    def get_itinerary_prompt() -> ChatPromptTemplate:
        """Prompt para crear itinerarios"""
        system_template = PromptManager.get_system_prompt() + """

Cuando se te pida crear un itinerario:
1. Estructura día por día
2. Incluye horarios recomendados
3. Distancias y tiempos de viaje
4. Nivel de dificultad
5. Artículos a llevar
6. Costo estimado
7. Alternativas según presupuesto"""
        
        human_template = "{itinerary_request}"
        
        system_message = SystemMessagePromptTemplate.from_template(system_template)
        human_message = HumanMessagePromptTemplate.from_template(human_template)
        
        return ChatPromptTemplate.from_messages([
            system_message,
            human_message
        ])


class PromptEngineer:
    """Ingeniero de prompts para optimización"""
    
    @staticmethod
    def add_context_to_prompt(base_prompt: str, context: Dict[str, Any]) -> str:
        """Añade contexto adicional a un prompt"""
        context_str = "\n\nContexto adicional:\n"
        for key, value in context.items():
            context_str += f"- {key}: {value}\n"
        return base_prompt + context_str
    
    @staticmethod
    def create_few_shot_prompt(examples: List[Dict[str, str]], task: str) -> str:
        """Crear prompt con ejemplos few-shot"""
        prompt = f"Tarea: {task}\n\nEjemplos:\n"
        
        for i, example in enumerate(examples, 1):
            prompt += f"\nEjemplo {i}:\n"
            for key, value in example.items():
                prompt += f"  {key}: {value}\n"
        
        prompt += "\nAhora responde la siguiente consulta:"
        return prompt
