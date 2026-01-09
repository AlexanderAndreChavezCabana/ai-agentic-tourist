"""
Módulo de utilidades generales
"""
import os
from typing import Dict, Any
from datetime import datetime


class Logger:
    """Logger simple para el chatbot"""
    
    @staticmethod
    def log(level: str, message: str) -> None:
        """Registrar un mensaje"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
    
    @staticmethod
    def info(message: str) -> None:
        """Log de información"""
        Logger.log("INFO", message)
    
    @staticmethod
    def error(message: str) -> None:
        """Log de error"""
        Logger.log("ERROR", message)
    
    @staticmethod
    def warning(message: str) -> None:
        """Log de advertencia"""
        Logger.log("WARNING", message)


class UserPreferences:
    """Gestor de preferencias del usuario"""
    
    def __init__(self):
        self.preferences = {
            "language": "es",
            "budget": "mid_range",
            "fitness_level": "medio",
            "interests": [],
            "restrictions": []
        }
    
    def set_preference(self, key: str, value: Any) -> None:
        """Establecer una preferencia"""
        self.preferences[key] = value
    
    def get_preference(self, key: str) -> Any:
        """Obtener una preferencia"""
        return self.preferences.get(key)
    
    def update_preferences(self, prefs: Dict[str, Any]) -> None:
        """Actualizar múltiples preferencias"""
        self.preferences.update(prefs)
    
    def get_all_preferences(self) -> Dict[str, Any]:
        """Obtener todas las preferencias"""
        return self.preferences.copy()


class APIRateLimiter:
    """Limitador de tasa para llamadas a API"""
    
    def __init__(self, max_calls: int = 10, time_window: int = 60):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
    
    def is_allowed(self) -> bool:
        """Verificar si una llamada está permitida"""
        import time
        current_time = time.time()
        
        # Limpiar llamadas antiguas
        self.calls = [call_time for call_time in self.calls 
                     if current_time - call_time < self.time_window]
        
        if len(self.calls) < self.max_calls:
            self.calls.append(current_time)
            return True
        
        return False
    
    def get_remaining_calls(self) -> int:
        """Obtener llamadas restantes"""
        return max(0, self.max_calls - len(self.calls))


class EnvironmentConfig:
    """Gestor de configuración desde variables de entorno"""
    
    @staticmethod
    def get_api_key(provider: str) -> str:
        """Obtener API key de un proveedor"""
        key_mapping = {
            "google": "GOOGLE_API_KEY"
        }
        
        env_var = key_mapping.get(provider.lower())
        if not env_var:
            raise ValueError(f"Proveedor desconocido: {provider}")
        
        api_key = os.getenv(env_var)
        if not api_key:
            raise ValueError(f"Variable de entorno {env_var} no configurada")
        
        return api_key
    
    @staticmethod
    def is_debug_mode() -> bool:
        """Verificar si está en modo debug"""
        return os.getenv("DEBUG", "false").lower() == "true"
    
    @staticmethod
    def get_log_level() -> str:
        """Obtener nivel de logging"""
        return os.getenv("LOG_LEVEL", "INFO")
