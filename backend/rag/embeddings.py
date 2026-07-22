import os
from dotenv import load_dotenv
from google import genai
from chromadb import EmbeddingFunction, Documents, Embeddings

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=input
        )
        return [e.values for e in response.embeddings]
