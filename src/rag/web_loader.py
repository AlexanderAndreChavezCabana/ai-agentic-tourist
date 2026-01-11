"""
Sistema RAG con WebBaseLoader para búsqueda híbrida
Carga contenido de páginas web y permite búsqueda semántica
"""
from typing import List, Dict, Any, Optional
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import os
from pathlib import Path
import pickle
import logging

logger = logging.getLogger(__name__)


class HuarazWebRAG:
    """Sistema RAG para contenido web de turismo en Huaraz"""
    
    # URLs de referencia para turismo en Huaraz
    TOURISM_URLS = [
        "https://www.huarazturismo.com/",
        "https://www.huarazturismo.com/tours",
        "https://www.huarazturismo.com/trekking",
        "https://www.huarazturismo.com/hoteles",
    ]
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Inicializar el sistema RAG.
        
        Args:
            openai_api_key: API key de OpenAI para embeddings
        """
        self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
        self.vector_store: Optional[FAISS] = None
        self.documents: List[Document] = []
        self.cache_dir = Path("data/rag_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "vector_store.pkl"
        
        # Configurar text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def load_web_content(self, urls: Optional[List[str]] = None, force_reload: bool = False) -> List[Document]:
        """
        Cargar contenido de páginas web.
        
        Args:
            urls: Lista de URLs a cargar (por defecto usa TOURISM_URLS)
            force_reload: Forzar recarga ignorando caché
        
        Returns:
            Lista de documentos cargados
        """
        urls = urls or self.TOURISM_URLS
        
        logger.info(f"Cargando contenido de {len(urls)} URLs...")
        documents = []
        
        for url in urls:
            try:
                logger.info(f"Procesando: {url}")
                loader = WebBaseLoader(
                    web_paths=[url],
                    bs_kwargs={
                        "parse_only": None,  # Parsear todo el contenido
                    }
                )
                docs = loader.load()
                
                # Añadir metadata
                for doc in docs:
                    doc.metadata['source'] = url
                    doc.metadata['type'] = 'web'
                
                documents.extend(docs)
                logger.info(f"✓ Cargado: {url} ({len(docs)} documentos)")
                
            except Exception as e:
                logger.error(f"✗ Error cargando {url}: {str(e)}")
                continue
        
        self.documents = documents
        logger.info(f"Total documentos cargados: {len(documents)}")
        return documents
    
    def create_vector_store(self, documents: Optional[List[Document]] = None) -> FAISS:
        """
        Crear vector store con embeddings.
        
        Args:
            documents: Documentos a procesar (usa self.documents si no se provee)
        
        Returns:
            Vector store FAISS
        """
        documents = documents or self.documents
        
        if not documents:
            raise ValueError("No hay documentos para crear el vector store")
        
        logger.info("Dividiendo documentos en chunks...")
        splits = self.text_splitter.split_documents(documents)
        logger.info(f"Total chunks creados: {len(splits)}")
        
        logger.info("Creando embeddings y vector store...")
        self.vector_store = FAISS.from_documents(
            documents=splits,
            embedding=self.embeddings
        )
        logger.info("✓ Vector store creado exitosamente")
        
        return self.vector_store
    
    def save_vector_store(self, path: Optional[Path] = None):
        """Guardar vector store en disco"""
        if not self.vector_store:
            raise ValueError("No hay vector store para guardar")
        
        path = path or self.cache_file
        logger.info(f"Guardando vector store en: {path}")
        
        self.vector_store.save_local(str(path.parent / "faiss_index"))
        
        # Guardar metadata de documentos
        with open(path, 'wb') as f:
            pickle.dump({
                'documents': self.documents,
                'timestamp': pd.Timestamp.now() if 'pd' in dir() else None
            }, f)
        
        logger.info("✓ Vector store guardado")
    
    def load_vector_store(self, path: Optional[Path] = None) -> bool:
        """
        Cargar vector store desde disco.
        
        Returns:
            True si se cargó exitosamente, False en caso contrario
        """
        path = path or self.cache_file
        index_path = path.parent / "faiss_index"
        
        if not index_path.exists():
            logger.warning(f"No se encontró vector store en: {index_path}")
            return False
        
        try:
            logger.info(f"Cargando vector store desde: {index_path}")
            self.vector_store = FAISS.load_local(
                str(index_path),
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            
            # Cargar metadata
            if path.exists():
                with open(path, 'rb') as f:
                    data = pickle.load(f)
                    self.documents = data.get('documents', [])
            
            logger.info("✓ Vector store cargado exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error cargando vector store: {str(e)}")
            return False
    
    def search(self, query: str, k: int = 4) -> List[Document]:
        """
        Buscar documentos relevantes.
        
        Args:
            query: Consulta de búsqueda
            k: Número de resultados a retornar
        
        Returns:
            Lista de documentos relevantes
        """
        if not self.vector_store:
            raise ValueError("Vector store no inicializado. Ejecuta create_vector_store() primero.")
        
        logger.info(f"Buscando: '{query}'")
        results = self.vector_store.similarity_search(query, k=k)
        logger.info(f"✓ Encontrados {len(results)} resultados")
        
        return results
    
    def search_with_score(self, query: str, k: int = 4) -> List[tuple]:
        """
        Buscar con scores de similitud.
        
        Args:
            query: Consulta de búsqueda
            k: Número de resultados
        
        Returns:
            Lista de tuplas (Document, score)
        """
        if not self.vector_store:
            raise ValueError("Vector store no inicializado")
        
        results = self.vector_store.similarity_search_with_score(query, k=k)
        return results
    
    def initialize(self, force_reload: bool = False) -> bool:
        """
        Inicializar el sistema RAG completo.
        
        Args:
            force_reload: Forzar recarga de contenido web
        
        Returns:
            True si se inicializó correctamente
        """
        try:
            # Intentar cargar desde caché
            if not force_reload and self.load_vector_store():
                logger.info("✓ Sistema RAG cargado desde caché")
                return True
            
            # Cargar contenido web
            logger.info("Cargando contenido web...")
            documents = self.load_web_content(force_reload=force_reload)
            
            if not documents:
                logger.warning("No se pudo cargar contenido web")
                return False
            
            # Crear vector store
            self.create_vector_store(documents)
            
            # Guardar en caché
            self.save_vector_store()
            
            logger.info("✓ Sistema RAG inicializado exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error inicializando sistema RAG: {str(e)}")
            return False


def format_search_results(results: List[Document]) -> str:
    """
    Formatear resultados de búsqueda para el agente.
    
    Args:
        results: Lista de documentos
    
    Returns:
        String formateado con los resultados
    """
    if not results:
        return "No se encontraron resultados relevantes."
    
    formatted = "📚 **Información encontrada:**\n\n"
    
    for i, doc in enumerate(results, 1):
        source = doc.metadata.get('source', 'Desconocido')
        content = doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content
        
        formatted += f"**{i}. Fuente: {source}**\n"
        formatted += f"{content}\n\n"
    
    return formatted
