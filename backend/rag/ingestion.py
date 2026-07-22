from rag.chunking import chunk_text
from rag.vector_store import get_collection
import uuid

def ingest_document(text: str, document_name: str, user_id: str):
    collection = get_collection()
    chunks = chunk_text(text)

    ids = [f"{user_id}_{document_name}_{i}_{uuid.uuid4().hex[:8]}" for i in range(len(chunks))]
    metadatas = [{"document_name": document_name, "user_id": user_id, "chunk_index": i} for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        ids=ids,
        metadatas=metadatas
    )

    return {"document_name": document_name, "chunks_stored": len(chunks)}
