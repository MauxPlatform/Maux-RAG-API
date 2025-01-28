from openai import OpenAI
from app.config.settings import settings
from app.services.base import BaseAIProvider
from typing import List, AsyncGenerator, Any

class OpenAIProvider(BaseAIProvider):
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def create_embedding(self, text: str) -> List[float]:
        result = self.client.embeddings.create(
            input=text,
            model=settings.OPENAI_EMBEDDING_MODEL
        )
        return result.data[0].embedding

    def create_chat_completion(self, messages: list, model: str = settings.CHAT_MODEL) -> Any:
        response = self.client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response
    
    def create_chat_completion_stream(self, messages: list, model: str = settings.CHAT_MODEL) -> AsyncGenerator[Any, None]:
        stream = self.client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )
        return stream

openai_service = OpenAIProvider() 