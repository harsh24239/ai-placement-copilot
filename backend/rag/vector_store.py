import chromadb
from rag.embeddings import GeminiEmbeddingFunction

chroma_client = chromadb.PersistentClient(path="./chroma_db")
embedding_function = GeminiEmbeddingFunction()

def get_collection(collection_name: str = "user_documents"):
    return chroma_client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )
