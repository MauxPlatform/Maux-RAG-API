from fastapi import FastAPI
from app.routes import vector_db, chat
import logging
from app.services.rag_service import rag_service

app = FastAPI(title="RAG API", description="API for RAG operations using ChromaDB and OpenAI")
logging.basicConfig(level=logging.INFO)

@app.on_event("startup")
async def startup_event():
    try:
        # Check if collection exists first
        collection = rag_service.chroma_service.get_or_create_collection(rag_service.collection_name)
        if not collection:
            rag_service.initialize_collection()
            logging.info("Vector database collection initialized successfully on startup")
        else:
            logging.info("Vector database collection already exists")
    except Exception as e:
        logging.error(f"Failed to initialize vector database collection: {str(e)}")

# Include routers with tags
app.include_router(vector_db.router, prefix="/v1/vector_db", tags=["Vector Database"])
app.include_router(chat.router, prefix="/v1", tags=["Chat"])

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the RAG API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)