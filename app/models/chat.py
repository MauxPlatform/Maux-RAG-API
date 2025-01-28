from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any

class ChatMessage(BaseModel):
    """A single message in a chat conversation"""
    role: Literal["system", "user", "assistant"] = Field(
        ...,
        description="The role of the message sender"
    )
    content: str = Field(
        ...,
        description="The content of the message"
    )

class ChatCompletionRequest(BaseModel):
    """Request model for chat completion"""
    model: str = Field(
        ...,
        description="The model to use for completion"
    )
    messages: List[ChatMessage] = Field(
        ...,
        description="The messages in the conversation"
    )
    max_tokens: Optional[int] = Field(
        None,
        description="The maximum number of tokens to generate"
    )
    stream: Optional[bool] = Field(
        False,
        description="Whether to stream the response"
    )

class ChatCompletionResponse(BaseModel):
    """Response model for chat completion"""
    id: str = Field(..., description="The unique identifier for this completion")
    object: str = Field(..., description="The object type")
    created: int = Field(..., description="The Unix timestamp of when this was created")
    model: str = Field(..., description="The model used for completion")
    choices: List[Dict[str, Any]] = Field(..., description="The completion choices")

class ChatCompletionStreamResponse(BaseModel):
    """Response model for streaming chat completion"""
    id: str = Field(..., description="The unique identifier for this chunk")
    object: str = Field(..., description="The object type")
    created: int = Field(..., description="The Unix timestamp of when this was created")
    model: str = Field(..., description="The model used for completion")
    choices: List[Dict[str, Any]] = Field(..., description="The completion choices for this chunk")
 
