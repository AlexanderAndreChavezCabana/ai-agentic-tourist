"""
FastAPI Backend para Chatbot Turístico Huaraz
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
from datetime import datetime
from pathlib import Path

# Importar el chatbot
import sys
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from main import ChatbotTouristico
from src.utils.helpers import Logger

# Inicializar FastAPI
app = FastAPI(
    title="Chatbot Turístico Huaraz",
    description="Asistente virtual para turismo en Huaraz, Perú",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
static_path = Path(__file__).parent / "static"
static_path.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Inicializar chatbot global
chatbot_instance = None

def get_chatbot():
    """Obtener instancia del chatbot"""
    global chatbot_instance
    if chatbot_instance is None:
        try:
            chatbot_instance = ChatbotTouristico(llm_provider="openai")
            Logger.info("Chatbot inicializado correctamente")
        except Exception as e:
            Logger.error(f"Error al inicializar chatbot: {e}")
            raise HTTPException(status_code=500, detail=f"Error al inicializar chatbot: {str(e)}")
    return chatbot_instance


# Modelos Pydantic
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = "default"


class ChatResponse(BaseModel):
    response: str
    timestamp: str
    session_id: str


# Almacenar conexiones WebSocket activas
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.conversation_history: Dict[str, List[Dict]] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    def add_to_history(self, session_id: str, role: str, content: str):
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
        self.conversation_history[session_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })


manager = ConnectionManager()


# Endpoints
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Servir la página principal"""
    html_file = static_path / "index.html"
    if html_file.exists():
        return FileResponse(html_file)
    return """
    <html>
        <head><title>Chatbot Turístico Huaraz</title></head>
        <body>
            <h1>Chatbot Turístico Huaraz</h1>
            <p>La interfaz está en desarrollo. Por favor, usa <a href="/docs">la API</a></p>
        </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """Verificar estado del servidor"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "chatbot_initialized": chatbot_instance is not None
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Endpoint para enviar mensajes al chatbot
    """
    try:
        chatbot = get_chatbot()
        response = chatbot.process_query(message.message)
        
        # Guardar en historial
        manager.add_to_history(message.session_id, "user", message.message)
        manager.add_to_history(message.session_id, "assistant", response)
        
        return ChatResponse(
            response=response,
            timestamp=datetime.now().isoformat(),
            session_id=message.session_id
        )
    except Exception as e:
        Logger.error(f"Error en /chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history/{session_id}")
async def get_history(session_id: str):
    """Obtener historial de conversación"""
    return {
        "session_id": session_id,
        "history": manager.conversation_history.get(session_id, [])
    }


@app.delete("/history/{session_id}")
async def clear_history(session_id: str):
    """Limpiar historial de conversación"""
    if session_id in manager.conversation_history:
        manager.conversation_history[session_id] = []
    return {"message": "Historial limpiado", "session_id": session_id}


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket para chat en tiempo real
    """
    await manager.connect(websocket)
    chatbot = get_chatbot()
    
    try:
        # Mensaje de bienvenida
        welcome_message = {
            "type": "system",
            "content": "¡Bienvenido al Chatbot Turístico de Huaraz! 🏔️ ¿En qué puedo ayudarte?",
            "timestamp": datetime.now().isoformat()
        }
        await manager.send_message(json.dumps(welcome_message), websocket)
        
        while True:
            # Recibir mensaje del cliente
            data = await websocket.receive_text()
            message_data = json.loads(data)
            user_message = message_data.get("message", "")
            
            if not user_message:
                continue
            
            # Guardar mensaje del usuario
            manager.add_to_history(session_id, "user", user_message)
            Logger.info(f"📩 Mensaje recibido de {session_id}: {user_message[:50]}...")
            
            # Procesar con el chatbot
            try:
                Logger.info("🤖 Procesando con el chatbot...")
                response = chatbot.process_query(user_message)
                Logger.info(f"✅ Respuesta generada: {response[:100]}...")
                
                manager.add_to_history(session_id, "assistant", response)
                
                # Enviar respuesta
                response_message = {
                    "type": "bot",
                    "content": response,
                    "timestamp": datetime.now().isoformat()
                }
                await manager.send_message(json.dumps(response_message), websocket)
                Logger.info("📤 Respuesta enviada al cliente")
                
            except Exception as e:
                Logger.error(f"❌ Error en WebSocket: {str(e)}")
                import traceback
                Logger.error(f"Traceback: {traceback.format_exc()}")
                
                error_message = {
                    "type": "error",
                    "content": f"Error al procesar tu mensaje: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                }
                await manager.send_message(json.dumps(error_message), websocket)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        Logger.info(f"WebSocket desconectado: {session_id}")
    except Exception as e:
        Logger.error(f"Error en WebSocket: {str(e)}")
        manager.disconnect(websocket)


@app.get("/attractions")
async def get_attractions():
    """Obtener lista de atracciones disponibles"""
    from data.knowledge.huaraz_knowledge import HuarazKnowledgeBase
    kb = HuarazKnowledgeBase()
    attractions = kb.get_all_attractions()
    
    return {
        "count": len(attractions),
        "attractions": [
            {
                "id": key,
                "name": attr.name,
                "description": attr.description,
                "altitude": attr.altitude,
                "difficulty": attr.difficulty,
                "duration": attr.duration
            }
            for key, attr in attractions.items()
        ]
    }


@app.get("/stats")
async def get_stats():
    """Obtener estadísticas de uso"""
    total_conversations = len(manager.conversation_history)
    total_messages = sum(len(msgs) for msgs in manager.conversation_history.values())
    
    return {
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "active_connections": len(manager.active_connections),
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    
    print("="*60)
    print("🏔️  CHATBOT TURÍSTICO HUARAZ - WEB INTERFACE".center(60))
    print("="*60)
    print("\n🚀 Iniciando servidor FastAPI...\n")
    print("📍 URL: http://localhost:8000")
    print("📚 Documentación: http://localhost:8000/docs")
    print("🔌 WebSocket: ws://localhost:8000/ws/tu_session_id")
    print("\n" + "="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
