from pydantic import BaseModel
from typing import List

class WeekPlan(BaseModel):
    week_number: int
    focus_area: str
    topics: List[str]
    daily_time_commitment: str

class Roadmap(BaseModel):
    total_weeks: int
    weeks: List[WeekPlan]
    summary: str
