from pydantic import BaseModel
from typing import List

class SkillGapAnalysis(BaseModel):
    matching_skills: List[str]
    missing_skills: List[str]
    fit_summary: str
