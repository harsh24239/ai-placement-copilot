import json
from config.llm import call_llm

SYSTEM_PROMPT = """You are a resume analysis expert. Given resume text, you will:
1. Give an ATS compatibility score out of 100
2. List key skills found in the resume
3. List common skills that seem to be missing (e.g. Python, SQL, Cloud, Git)

Respond ONLY with valid JSON in this exact format, no other text:
{
  "ats_score": <number>,
  "skills_found": [<strings>],
  "skills_missing": [<strings>]
}
"""

def analyze_resume(resume_text: str) -> dict:
    raw_response = call_llm(SYSTEM_PROMPT, resume_text)
    cleaned = raw_response.replace("```json", "").replace("```", "").strip()
    return json.loads(cleaned)
