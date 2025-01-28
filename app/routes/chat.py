from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.chat import ChatCompletionRequest
from app.services.core.rag_service import rag_service
import json

router = APIRouter()

@router.post("/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest):
    try:
        # Get the last user message for context search
        last_message = next((msg for msg in reversed(request.messages) if msg.role == "user"), None)
        if not last_message:
            raise HTTPException(status_code=400, detail="No user message found in the conversation")
        
        # Create embedding for the last user message using the configured provider
        embedding = rag_service.provider.create_embedding(last_message.content)
        search_results = rag_service.search_similar_documents(embedding)
        
        # Build context from search results
        context = "Relevant documents:\n"
        for doc, metadata in zip(search_results['documents'][0], search_results['metadatas'][0]):
            context += f"- Content: {doc}\n"
            context += f"  Metadata: {metadata}\n"

        if request.stream:
            async def stream_response():
                async for chunk in rag_service.generate_stream_response(
                    messages=request.messages,
                    context=context,
                    model=request.model
                ):
                    yield f"data: {chunk}\n\n"
                yield "data: [DONE]\n\n"

            return StreamingResponse(
                stream_response(),
                media_type="text/event-stream"
            )
        # Otherwise return the complete response
        response = rag_service.generate_response(
            messages=request.messages,
            context=context,
            model=request.model
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat completion failed: {str(e)}")

