import json
from config.llm import call_llm
from models.roadmap import Roadmap

SYSTEM_PROMPT = """You are a study roadmap planner for a job candidate preparing for a specific role.
Given a list of missing skills and the candidate's available weeks to prepare, create a realistic,
week-by-week study roadmap.

Rules:
- Group related skills into the same week where sensible (e.g. don't separate "AWS" and "Cloud Platforms" into different weeks)
- Order weeks by priority — most critical/foundational skills first
- Each week should have a realistic daily time commitment (e.g. "1-2 hours/day")
- Be specific with topics, not vague (e.g. "AWS EC2 basics, S3 storage" not just "learn AWS")

Respond ONLY with valid JSON in this exact format, no other text:
{
  "total_weeks": <number>,
  "weeks": [
    {
      "week_number": <number>,
      "focus_area": "<short theme for this week>",
      "topics": [<specific topic strings>],
      "daily_time_commitment": "<string>"
    }
  ],
  "summary": "<one paragraph overview of the plan and expected outcome>"
}
"""

def create_roadmap(missing_skills: list, available_weeks: int = 4) -> dict:
    user_message = f"""
Missing skills to cover: {missing_skills}
Available weeks to prepare: {available_weeks}
"""
    raw_response = call_llm(SYSTEM_PROMPT, user_message)
    cleaned = raw_response.replace("```json", "").replace("```", "").strip()
    parsed = json.loads(cleaned)
    validated = Roadmap(**parsed)
    return validated.model_dump()
