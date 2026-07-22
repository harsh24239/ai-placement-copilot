import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def call_llm(system_prompt: str, user_message: str, model: str = "gemini-flash-latest") -> str:
    """
    Sends a system + user message to Gemini and returns the raw text response.
    """
    response = client.models.generate_content(
        model=model,
        contents=user_message,
        config={"system_instruction": system_prompt}
    )
    return response.text
