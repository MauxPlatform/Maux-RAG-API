import requests
from app.config.settings import settings

class AvalaiService:
    def __init__(self):
        self.base_url = settings.AVALAI_BASE_URL
        self.defualt_embedding_model = "text-embedding"
        self.defualt_chat_model = "chat-completion"

    def create_embedding(self, text:str):
        response = requests.post(
            f"{self.base_url}/embedding",
            json={"input": text, "model": self.default_embedding_model}
        )

    def create_chat_completion(self, messages: list, model: str = None):
        response = requests.post(
            f"{self.base_url}/chat/completions",
            json={"messages": messages, "model": model or self.default_chat_model}
        )
        response.raise_for_status()
        return response.json()
    
    def create_chat_completion_stream(self, messages: list, model: str = None):
        response = requests.post(
            f"{self.base_url}/chat/completions",
            json={"messages": messages, "model": model or self.default_chat_model, "stream": True},
            stream=True
        )
        response.raise_for_status()
        for chunk in response.iter_lines():
            yield chunk.decode("utf-8")