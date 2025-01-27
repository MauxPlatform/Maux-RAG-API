from app.services.chroma_service import ChromaService
from app.services.openai_service import openai_service
from app.services.avalai_service import AvalaiService
import uuid
from typing import AsyncGenerator
import json
from app.config.settings import settings
class RAGService:
    def __init__(self):
        self.collection_name = "RAG_COLLECTION"
        self.chroma_service = ChromaService()

        if settings.PROVIDER == "openai":
            self.provider_service = openai_service
        elif settings.PROVIDER == "avalai":
            self.provider_service = AvalaiService()
        else:
            raise ValueError("Invalid provider selected")

    def initialize_collection(self):
        self.chroma_service.create_collection(self.collection_name)

    def add_document(self, text: str, metadata: dict = None):
        self.chroma_service.add_documents(
            collection_name=self.collection_name,
            documents=[text],
            ids=[f"doc_{uuid.uuid4()}"],
            metadatas=[metadata] if metadata else None
        )
    def clear_collection(self):
        self.chroma_service.clear_collection(self.collection_name)
    def search_similar_documents(self, embedding: list):
        results = self.chroma_service.search(
            collection_name=self.collection_name,
            query_embeddings=embedding,
        )
        return results
    
    def generate_response(self, messages: list, context: str, model: str = settings.CHAT_MODEL):
        messages_with_context = messages.copy()
        system_msg = next((msg for msg in messages_with_context if msg.role == "system"), None)
        
        if system_msg:
            # Append context to existing system message
            system_msg.content = f"{system_msg.content}\n\nUse this context to answer the question:\n{context}"
        else:
            # Create new system message with context
            messages_with_context.insert(0, {
                "role": "system",
                "content": f"Use this context to enhance your responses:\n{context}"
            })

        # Convert Pydantic models to dictionaries for OpenAI API
        messages_dict = [msg.model_dump() for msg in messages_with_context]
        return openai_service.create_chat_completion(messages_dict, model)

    async def generate_stream_response(self, messages: list, context: str, model: str = settings.CHAT_MODEL) -> AsyncGenerator[str, None]:
        messages_with_context = messages.copy()
        system_msg = next((msg for msg in messages_with_context if msg.role == "system"), None)
        
        if system_msg:
            # Append context to existing system message
            system_msg.content = f"{system_msg.content}\n\nUse this context to answer the question:\n{context}"
        else:
            # Create new system message with context
            messages_with_context.insert(0, {
                "role": "system",
                "content": f"Use this context to enhance your responses:\n{context}"
            })
        
        # Convert Pydantic models to dictionaries for OpenAI API
        messages_dict = [msg.model_dump() for msg in messages_with_context]
        stream = openai_service.create_chat_completion_stream(messages_dict, model)
        for chunk in stream:
            yield json.dumps({
                "choices": [
                    {
                        "delta": {
                            "content": chunk.choices[0].delta.content,
                            "role": chunk.choices[0].delta.role if hasattr(chunk.choices[0].delta, 'role') else None,
                            "function_call": chunk.choices[0].delta.function_call if hasattr(chunk.choices[0].delta, 'function_call') else None
                        }
                    }
                ],
                "model": chunk.model,
                "object": chunk.object,
                "created": chunk.created,
                "id": chunk.id
            })

rag_service = RAGService()