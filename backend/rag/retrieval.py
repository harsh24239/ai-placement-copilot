from rag.vector_store import get_collection

def retrieve_relevant_chunks(query: str, user_id: str, top_k: int = 3) -> list[str]:
    collection = get_collection()
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        where={"user_id": user_id}
    )
    return results["documents"][0] if results["documents"] else []
