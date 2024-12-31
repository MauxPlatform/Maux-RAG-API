from openai import OpenAI
from app.config.settings import settings

class OpenAIService:
    def __init__(self):


        # you can change this to use the AVALAI API
        # self.client = OpenAI(api_key=settings.AVALAI_API_KEY , base_url="https://api.avalapis.ir/v1")
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY )

    def create_embedding(self, text: str):
        result = self.client.embeddings.create(
            input=text,
            model=settings.OPENAI_EMBEDDING_MODEL
        )
        embedding = result.data[0].embedding
        return embedding

    def create_chat_completion(self, messages: list, model: str = settings.CHAT_MODEL):
        response = self.client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response
    
    def create_chat_completion_stream(self, messages: list, model: str = settings.CHAT_MODEL):
        stream = self.client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )
        return stream

openai_service = OpenAIService()