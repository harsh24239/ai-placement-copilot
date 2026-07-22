from config.llm import call_llm
from memory.session_manager import get_session

SYSTEM_PROMPT = """You are a technical interviewer conducting a mock coding interview.
Ask one question at a time. After the candidate answers, evaluate their answer briefly,
then ask a relevant follow-up question that builds on their previous answers.

Keep your responses conversational and concise, like a real interviewer would.
Do not ask more than one question per turn.
"""


def start_interview(session_id: str, topic: str) -> str:
    memory = get_session(session_id)
    if memory is None:
        raise ValueError("Invalid session_id")

    opening_message = f"Let's start a mock interview focused on {topic}. Please begin."
    memory.add_message("user", opening_message)

    question = call_llm(SYSTEM_PROMPT, opening_message)
    memory.add_message("assistant", question)

    return question


def continue_interview(session_id: str, candidate_answer: str) -> str:
    memory = get_session(session_id)
    if memory is None:
        raise ValueError("Invalid session_id")

    memory.add_message("user", candidate_answer)

    # Build the full conversation history as context for this turn
    history_text = "\n".join(
        f"{msg['role'].upper()}: {msg['content']}" for msg in memory.get_history()
    )

    response = call_llm(SYSTEM_PROMPT, history_text)
    memory.add_message("assistant", response)

    return response
