import json
from config.llm import call_llm
from models.jd import JobDescriptionAnalysis

SYSTEM_PROMPT = """You are a job description analysis expert. Given job description text, extract:
1. The job title
2. The company name (if mentioned)
3. Required technical skills (programming languages, frameworks, tools)
4. Required soft skills (communication, teamwork, etc.)
5. Experience level (e.g. Internship, Entry-level, Mid-level, Senior)

Respond ONLY with valid JSON in this exact format, no other text:
{
  "job_title": "<string>",
  "company": "<string or null if not mentioned>",
  "technical_skills": [<strings>],
  "soft_skills": [<strings>],
  "experience_level": "<string>"
}
"""

def analyze_jd(jd_text: str) -> dict:
    raw_response = call_llm(SYSTEM_PROMPT, jd_text)
    cleaned = raw_response.replace("```json", "").replace("```", "").strip()
    parsed = json.loads(cleaned)
    validated = JobDescriptionAnalysis(**parsed)
    return validated.model_dump()
