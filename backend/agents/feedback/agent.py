import json
from config.llm import call_llm
from memory.session_manager import get_session
from models.feedback import InterviewFeedback

SYSTEM_PROMPT = """You are an interview evaluator. Given a full mock interview transcript, assess
the candidate's performance.

Score each of these from 1-10:
- confidence_score: how confident and decisive their answers sounded
- technical_accuracy_score: how technically correct their answers were
- communication_score: how clearly they explained their reasoning

Also identify weak_topics: specific technical topics they struggled with, based on the transcript.

Respond ONLY with valid JSON in this exact format, no other text:
{
  "confidence_score": <1-10>,
  "technical_accuracy_score": <1-10>,
  "communication_score": <1-10>,
  "weak_topics": [<strings>],
  "overall_feedback": "<one paragraph of constructive feedback>"
}
"""

def generate_feedback(session_id: str) -> dict:
    memory = get_session(session_id)
    if memory is None:
        raise ValueError("Invalid session_id")

    transcript = "\n".join(
        f"{msg['role'].upper()}: {msg['content']}" for msg in memory.get_history()
    )

    raw_response = call_llm(SYSTEM_PROMPT, transcript)
    cleaned = raw_response.replace("```json", "").replace("```", "").strip()
    parsed = json.loads(cleaned)
    validated = InterviewFeedback(**parsed)
    return validated.model_dump()
