from fastapi import APIRouter, HTTPException
from app.models.embedding import Document, Query, SearchResult
from app.services.core.rag_service import rag_service
from typing import List

router = APIRouter()


# this route is used to initialize the collection in the vector database, you need to call it before you can use the other routes
@router.post("/initialize_collection", status_code=201)
async def initialize_collection():
    try:
        rag_service.initialize_collection()
        return {"message": "Collection initialized successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize collection: {str(e)}")

# this route is used to add a document to the vector database
@router.post("/add_document", status_code=201, response_model=dict)
async def add_document(document: Document):
    try:
        rag_service.add_document(document.text, document.metadata)
        return {"message": "Document embedded and added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to embed and add document: {str(e)}")

# this route is used to search for similar documents in the vector database
@router.post("/search_documents", response_model=List[SearchResult])
async def search_documents(query: Query):
    try:
        # Use the configured provider for embeddings
        embedding = rag_service.provider.create_embedding(query.text)
        results = rag_service.search_similar_documents(embedding)
        search_results = []
        for i in range(len(results['ids'][0])):
            search_results.append(SearchResult(
                id=i,  # Using index as id instead of the UUID
                text=results['documents'][0][i],
                metadata=results['metadatas'][0][i]
            ))
        return search_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
    

# this route is used to clear the collection in the vector database
@router.delete("/clear_collection")
async def clear_collection():
    try:
        rag_service.clear_collection()
        return {"message": "Collection cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear collection: {str(e)}")

