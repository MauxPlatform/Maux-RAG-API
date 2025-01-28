from pydantic_settings import BaseSettings
from typing import Literal, Optional
from functools import lru_cache

class Settings(BaseSettings):
    # AI Provider Settings
    PROVIDER: Literal["openai", "avalai"] = "openai"
    
    # OpenAI Settings
    OPENAI_API_KEY: str
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    CHAT_MODEL: str = "gpt-4o-mini"
    
    # AvalAI Settings / میتوانید از وب سرویس aval ai استفاده کنید
    AVALAI_API_KEY: Optional[str] = None
    AVALAI_BASE_URL: str = "https://api.avalapis.ir/v1"
    
    # Vector Store Settings
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
    RAG_SEARCH_LIMIT: int = 3
    
    # System Settings
    SYSTEM_PROMPT: str = (
        "You are a helpful assistant. Use the provided context to answer "
        "the user's question. If the context is not relevant, just say 'I don't know'"
    )

    class Config:
        env_file = ".env"
        case_sensitive = True

    def validate_api_keys(self):
        """Validate that the required API key is present based on the selected provider"""
        if self.PROVIDER == "avalai" and not self.AVALAI_API_KEY:
            raise ValueError("AVALAI_API_KEY is required when using AvalAI provider")
        elif self.PROVIDER == "openai" and not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required when using OpenAI provider")

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    settings = Settings()
    settings.validate_api_keys()
    return settings

settings = get_settings()