from abc import ABC, abstractmethod
from typing import List, AsyncGenerator, Dict, Any

class BaseAIProvider(ABC):
    @abstractmethod
    def create_embedding(self, text: str) -> List[float]:
        pass

    @abstractmethod
    def create_chat_completion(self, messages: list, model: str) -> Any:
        pass
    
    @abstractmethod
    def create_chat_completion_stream(self, messages: list, model: str) -> AsyncGenerator[Any, None]:
        pass 