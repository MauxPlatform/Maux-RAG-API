from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    # A directory to store the chroma db
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
    # The model to use for embedding, WE RECOMMEND NOT CHANGING THIS
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    # The model to use for chat completion
    CHAT_MODEL: str = "gpt-4o-mini"
    # The number of documents to search for similar documents in the vector database
    RAG_SEARCH_LIMIT: int = 3
    # The system prompt to use for chat completion, you can change it to make the assistant more helpful for your use case
    SYSTEM_PROMPT: str = "You are a helpful assistant. Use the provided context to answer the user's question. If the context is not relevant, just say 'I don't know'"
    # AvalAI
    AVALAI_BASE_URL: str = "https://api.avalapis.ir/v1"
    PROVIDER: str = "avalai"

    class Config:
        env_file = ".env"

settings = Settings()