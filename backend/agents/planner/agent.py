import json
from config.llm import call_llm
from models.plan import Plan

SYSTEM_PROMPT = """You are a planning agent for a career-prep assistant. Given a user's goal in plain
English, decide which of the following steps are needed to help them, in what order.

Available steps (use these exact names):
- "resume_analysis" — score and analyze the candidate's resume
- "jd_analysis" — extract requirements from a job description
- "skill_gap" — compare resume vs JD to find missing skills
- "roadmap" — build a personalized study plan (requires skill_gap to have run first)
- "mock_interview" — run a mock interview

Only include steps that are actually relevant to the user's stated goal. For example, if the user
only uploaded a resume with no job description, do not include "jd_analysis" or "skill_gap".

Respond ONLY with valid JSON in this exact format, no other text:
{
  "goal_summary": "<one sentence restating what the user wants>",
  "steps": [<ordered list of step name strings from the list above>],
  "reasoning": "<short explanation of why these steps, in this order>"
}
"""

def create_plan(user_goal: str, has_resume: bool, has_jd: bool) -> dict:
    user_message = f"""
User's goal: {user_goal}
Resume uploaded: {has_resume}
Job description uploaded: {has_jd}
"""
    raw_response = call_llm(SYSTEM_PROMPT, user_message)
    cleaned = raw_response.replace("```json", "").replace("```", "").strip()
    parsed = json.loads(cleaned)
    validated = Plan(**parsed)
    return validated.model_dump()
