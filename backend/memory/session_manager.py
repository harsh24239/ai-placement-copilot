from memory.short_term import ConversationMemory
import uuid

# In-memory store: session_id -> ConversationMemory instance
# NOTE: this resets if the server restarts — genuinely short-term, by design.
active_sessions: dict[str, ConversationMemory] = {}


def create_session() -> str:
    session_id = str(uuid.uuid4())
    active_sessions[session_id] = ConversationMemory()
    return session_id


def get_session(session_id: str) -> ConversationMemory | None:
    return active_sessions.get(session_id)
