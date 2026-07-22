from config.llm import call_llm
from rag.retrieval import retrieve_relevant_chunks

SYSTEM_PROMPT = """You are a helpful study assistant. Answer the user's question using ONLY the
provided context from their own uploaded notes. If the context doesn't contain enough information
to answer the question, say so honestly rather than making something up.

Do not mention "the context" or "the provided text" in your answer — just answer naturally as if
you know this from the material.
"""

def answer_from_documents(question: str, user_id: str) -> dict:
    relevant_chunks = retrieve_relevant_chunks(question, user_id, top_k=3)

    if not relevant_chunks:
        return {
            "answer": "I don't have any uploaded documents to answer this from yet. Please upload some notes first.",
            "sources_used": 0
        }

    context = "\n\n---\n\n".join(relevant_chunks)
    user_message = f"""
Context from the user's uploaded notes:
{context}

Question: {question}
"""

    answer = call_llm(SYSTEM_PROMPT, user_message)

    return {
        "answer": answer,
        "sources_used": len(relevant_chunks)
    }
