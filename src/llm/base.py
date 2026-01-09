"""
Módulo de clientes LLM - Integración con Google AI
"""
import os
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_model import BaseLanguageModel


class LLMClient(ABC):
    """Clase base para clientes LLM"""
    
    @abstractmethod
    def get_model(self) -> BaseLanguageModel:
        """Obtener instancia del modelo"""
        pass


class GoogleAIClient(LLMClient):
    """Cliente para Google AI (Gemini)"""
    
    def __init__(
        self,
        model_name: str = "gemini-pro",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        api_key: Optional[str] = None
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
    
    def get_model(self) -> BaseLanguageModel:
        return ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=self.temperature,
            max_output_tokens=self.max_tokens,
            google_api_key=self.api_key
        )


class LLMFactory:
    """Factory para crear clientes LLM"""
    
    _clients: Dict[str, LLMClient] = {
        "google": GoogleAIClient,
    }
    
    @classmethod
    def create_client(cls, provider: str, **kwargs) -> LLMClient:
        """Crear cliente LLM por proveedor"""
        if provider not in cls._clients:
            raise ValueError(f"Proveedor no soportado: {provider}")
        
        client_class = cls._clients[provider]
        return client_class(**kwargs)
    
    @classmethod
    def get_model(cls, provider: str, **kwargs) -> BaseLanguageModel:
        """Obtener modelo LLM directo"""
        client = cls.create_client(provider, **kwargs)
        return client.get_model()
