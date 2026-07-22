class ConversationMemory:
    """
    Simple in-memory conversation history for a single session.
    Lives only as long as the Python process runs — intentionally NOT persisted to disk.
    """
    def __init__(self):
        self.messages = []

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def get_history(self):
        return self.messages

    def clear(self):
        self.messages = []
