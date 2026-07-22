from pydantic import BaseModel
from typing import List

class Plan(BaseModel):
    goal_summary: str
    steps: List[str]
    reasoning: str
