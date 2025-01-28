from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Document(BaseModel):
    """A document to be embedded and stored"""
    text: str = Field(
        ...,
        description="The text content of the document"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional metadata associated with the document"
    )

class Query(BaseModel):
    """A query for semantic search"""
    prompt: str = Field(
        ...,
        description="The search query text"
    )

class SearchResult(BaseModel):
    """A single search result"""
    id: int = Field(
        ...,
        description="The unique identifier of the result"
    )
    text: str = Field(
        ...,
        description="The text content of the result"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional metadata associated with the result"
    )
    score: Optional[float] = Field(
        None,
        description="The similarity score of the result"
    )

class EmbeddingResponse(BaseModel):
    """Response containing generated embeddings"""
    embedding: List[float] = Field(
        ...,
        description="The generated embedding vector"
    )
    model: Optional[str] = Field(
        None,
        description="The model used to generate the embedding"
    )
    usage: Optional[Dict[str, int]] = Field(
        None,
        description="Token usage information"
    )