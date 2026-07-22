import json
from config.llm import call_llm
from models.skill_gap import SkillGapAnalysis

SYSTEM_PROMPT = """You are a career skill-gap analyst. You will be given:
1. Skills the candidate already has (from their resume)
2. Skills required by a job description

Compare them intelligently — treat similar terms as matches (e.g. "Node.js" and "NodeJS" are the same,
"Java" implies basic OOP knowledge). Then produce:
1. Skills the candidate already has that match job requirements
2. Skills the candidate is missing, ordered by importance (most critical first)
3. A short one-paragraph summary of the candidate's overall fit for this role

Respond ONLY with valid JSON in this exact format, no other text:
{
  "matching_skills": [<strings>],
  "missing_skills": [<strings>],
  "fit_summary": "<string>"
}
"""

def analyze_skill_gap(resume_skills: list, jd_technical_skills: list, jd_soft_skills: list) -> dict:
    # Step A: quick deterministic pre-pass using plain Python (fast, free, exact matches only)
    resume_set = set(s.lower().strip() for s in resume_skills)
    required_set = set(s.lower().strip() for s in jd_technical_skills + jd_soft_skills)
    exact_matches = resume_set & required_set
    exact_missing = required_set - resume_set

    # Step B: hand both raw lists + our rough pre-pass to the LLM for the smarter final judgment
    user_message = f"""
Candidate's resume skills: {resume_skills}
Job's required technical skills: {jd_technical_skills}
Job's required soft skills: {jd_soft_skills}

Our rough automated pre-check found these exact-text matches: {list(exact_matches)}
And these possibly missing: {list(exact_missing)}

Now give your smarter final analysis, catching any near-matches our rough check missed.
"""
    raw_response = call_llm(SYSTEM_PROMPT, user_message)
    cleaned = raw_response.replace("```json", "").replace("```", "").strip()
    parsed = json.loads(cleaned)
    validated = SkillGapAnalysis(**parsed)
    return validated.model_dump()
