from pydantic import BaseModel
from typing import Optional, List

class JobDescriptionAnalysis(BaseModel):
    job_title: str
    company: Optional[str] = None
    technical_skills: List[str]
    soft_skills: List[str]
    experience_level: str
