import chromadb
from chromadb.config import Settings as ChromaSettings
import chromadb.utils.embedding_functions as embedding_functions
from typing import List, Dict, Any, Optional
from app.config.settings import settings
from app.services.providers.openai_service import OpenAIProvider
from app.services.providers.avalai_service import AvalaiProvider

class VectorStoreService:
    def __init__(self):
        # Initialize the appropriate embedding function based on provider
        if settings.PROVIDER == "openai":
            self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
                api_key=settings.OPENAI_API_KEY,
                model_name=settings.OPENAI_EMBEDDING_MODEL
            )
        elif settings.PROVIDER == "avalai":
            self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
                api_key=settings.AVALAI_API_KEY,
                api_base=settings.AVALAI_BASE_URL,
                model_name=settings.OPENAI_EMBEDDING_MODEL
            )
        else:
            raise ValueError(f"Unsupported provider: {settings.PROVIDER}")
            
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIRECTORY,
            settings=ChromaSettings(
                allow_reset=True,
                anonymized_telemetry=False
            )
        )

    def create_collection(self, collection_name: str):
        """Create a new collection or get existing one"""
        try:
            return self.client.create_collection(
                name=collection_name, 
                embedding_function=self.embedding_function
            )
        except ValueError as e:
            if "Collection already exists" in str(e):
                return self.get_collection(collection_name)
            raise e

    def get_collection(self, collection_name: str):
        """Get an existing collection"""
        return self.client.get_collection(
            name=collection_name, 
            embedding_function=self.embedding_function
        )

    def get_or_create_collection(self, collection_name: str):
        """Get an existing collection or create a new one"""
        return self.client.get_or_create_collection(
            name=collection_name, 
            embedding_function=self.embedding_function
        )

    def add_documents(
        self, 
        collection_name: str, 
        documents: List[str], 
        ids: List[str], 
        metadatas: Optional[List[Dict[str, Any]]] = None
    ):
        """Add documents to a collection"""
        collection = self.get_or_create_collection(collection_name)
        return collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )

    def search(
        self, 
        collection_name: str, 
        query_embeddings: List[float]
    ) -> Dict[str, Any]:
        """Search for similar documents in a collection"""
        collection = self.get_or_create_collection(collection_name)
        return collection.query(
            query_embeddings=query_embeddings,
            n_results=settings.RAG_SEARCH_LIMIT
        )

    def clear_collection(self, collection_name: str):
        """Delete a collection"""
        collection = self.get_or_create_collection(collection_name)
        return collection.delete() 