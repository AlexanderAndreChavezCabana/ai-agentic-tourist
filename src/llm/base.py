"""
Módulo de clientes LLM - Integración con OpenAI
"""
import os
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

from langchain_openai import ChatOpenAI


class LLMClient(ABC):
    """Clase base para clientes LLM"""
    
    @abstractmethod
    def get_model(self) -> Any:
        """Obtener instancia del modelo"""
        pass


class OpenAIClient(LLMClient):
    """Cliente para OpenAI (GPT-4)"""
    
    def __init__(
        self,
        model_name: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        api_key: Optional[str] = None
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
    
    def get_model(self) -> Any:
        return ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            openai_api_key=self.api_key
        )


class LLMFactory:
    """Factory para crear clientes LLM"""
    
    _clients: Dict[str, LLMClient] = {
        "openai": OpenAIClient,
    }
    
    @classmethod
    def create_client(cls, provider: str, **kwargs) -> LLMClient:
        """Crear cliente LLM por proveedor"""
        if provider not in cls._clients:
            raise ValueError(f"Proveedor no soportado: {provider}")
        
        client_class = cls._clients[provider]
        return client_class(**kwargs)
    
    @classmethod
    def get_model(cls, provider: str, **kwargs) -> Any:
        """Obtener modelo LLM directo"""
        client = cls.create_client(provider, **kwargs)
        return client.get_model()
