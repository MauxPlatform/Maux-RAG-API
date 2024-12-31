import chromadb
from chromadb.config import Settings as ChromaSettings
from app.config.settings import settings

import chromadb.utils.embedding_functions as embedding_functions
class ChromaService:
    def __init__(self):
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=settings.OPENAI_API_KEY,
            model_name=settings.OPENAI_EMBEDDING_MODEL
        )
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIRECTORY,
            settings=ChromaSettings(
                allow_reset=True,
                anonymized_telemetry=False
            )
        )

    def create_collection(self, collection_name: str):
        try:
            return self.client.create_collection(name=collection_name, embedding_function=self.embedding_function)
        except ValueError as e:
            if "Collection already exists" in str(e):
                return self.client.get_collection(name=collection_name, embedding_function=self.embedding_function)
            raise e

    def get_or_create_collection(self, collection_name: str):
        return self.client.get_or_create_collection(name=collection_name, embedding_function=self.embedding_function)

    def add_documents(self, collection_name: str, documents: list, ids: list, metadatas: list = None):
        collection = self.get_or_create_collection(collection_name)
        return collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )

    def search(self, collection_name: str, query_embeddings: list):
        collection = self.get_or_create_collection(collection_name)
        return collection.query(
            query_embeddings=query_embeddings,
            n_results=settings.RAG_SEARCH_LIMIT
        )
    def clear_collection(self, collection_name: str):
        collection = self.get_or_create_collection(collection_name)
        return collection.delete()