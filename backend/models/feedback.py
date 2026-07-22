from pydantic import BaseModel
from typing import List

class InterviewFeedback(BaseModel):
    confidence_score: int
    technical_accuracy_score: int
    communication_score: int
    weak_topics: List[str]
    overall_feedback: str
