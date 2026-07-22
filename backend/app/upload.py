from fastapi import APIRouter, UploadFile, File, HTTPException
from tools.pdf_reader import extract_text_from_pdf
from agents.resume.agent import analyze_resume

router = APIRouter()

@router.post("/upload/resume")
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    file_bytes = await file.read()
    text = extract_text_from_pdf(file_bytes)

    return {
        "filename": file.filename,
        "character_count": len(text),
        "preview": text[:300]
    }

@router.post("/upload/jd")
async def upload_jd(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    file_bytes = await file.read()
    text = extract_text_from_pdf(file_bytes)

    return {
        "filename": file.filename,
        "character_count": len(text),
        "preview": text[:300]
    }

@router.post("/analyze/resume")
async def analyze_resume_endpoint(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    file_bytes = await file.read()
    text = extract_text_from_pdf(file_bytes)
    analysis = analyze_resume(text)
    return analysis
from agents.job_description.agent import analyze_jd

@router.post("/analyze/jd")
async def analyze_jd_endpoint(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    file_bytes = await file.read()
    text = extract_text_from_pdf(file_bytes)
    analysis = analyze_jd(text)
    return analysis

from agents.skill_gap.agent import analyze_skill_gap

@router.post("/analyze/full")
async def analyze_full_endpoint(
    resume_file: UploadFile = File(...),
    jd_file: UploadFile = File(...)
):
    if resume_file.content_type != "application/pdf" or jd_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    resume_bytes = await resume_file.read()
    jd_bytes = await jd_file.read()

    resume_text = extract_text_from_pdf(resume_bytes)
    jd_text = extract_text_from_pdf(jd_bytes)

    resume_analysis = analyze_resume(resume_text)
    jd_analysis = analyze_jd(jd_text)

    skill_gap = analyze_skill_gap(
        resume_skills=resume_analysis["skills_found"],
        jd_technical_skills=jd_analysis["technical_skills"],
        jd_soft_skills=jd_analysis["soft_skills"]
    )

    return {
        "resume_analysis": resume_analysis,
        "jd_analysis": jd_analysis,
        "skill_gap": skill_gap
    }

from workflows.placement_workflow import placement_graph

@router.post("/workflow/placement")
async def run_placement_workflow(
    resume_file: UploadFile = File(...),
    jd_file: UploadFile = File(...)
):
    if resume_file.content_type != "application/pdf" or jd_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    resume_bytes = await resume_file.read()
    jd_bytes = await jd_file.read()

    result = placement_graph.invoke({
        "resume_bytes": resume_bytes,
        "jd_bytes": jd_bytes
    })

    return {
        "resume_analysis": result["resume_analysis"],
        "jd_analysis": result["jd_analysis"],
        "skill_gap": result["skill_gap"]
    }

from agents.planner.agent import create_plan
from pydantic import BaseModel

class PlanRequest(BaseModel):
    user_goal: str
    has_resume: bool = False
    has_jd: bool = False

@router.post("/plan")
async def plan_endpoint(request: PlanRequest):
    plan = create_plan(request.user_goal, request.has_resume, request.has_jd)
    return plan

from agents.roadmap.agent import create_roadmap

class RoadmapRequest(BaseModel):
    missing_skills: list[str]
    available_weeks: int = 4

@router.post("/roadmap")
async def roadmap_endpoint(request: RoadmapRequest):
    roadmap = create_roadmap(request.missing_skills, request.available_weeks)
    return roadmap

from memory.long_term import save_progress, get_progress

class SaveProgressRequest(BaseModel):
    user_id: str
    resume_ats_score: float = None
    weak_topics: list[str] = None
    session_summary: str = None

@router.post("/memory/save")
async def save_progress_endpoint(request: SaveProgressRequest):
    save_progress(
        user_id=request.user_id,
        resume_ats_score=request.resume_ats_score,
        weak_topics=request.weak_topics,
        session_summary=request.session_summary
    )
    return {"status": "saved"}

@router.get("/memory/{user_id}")
async def get_progress_endpoint(user_id: str):
    progress = get_progress(user_id)
    if progress is None:
        return {"status": "no_history", "message": "No prior sessions found for this user"}
    return progress

from rag.ingestion import ingest_document
from agents.rag_qa.agent import answer_from_documents

@router.post("/rag/ingest")
async def ingest_endpoint(
    file: UploadFile = File(...),
    user_id: str = "harsh"
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    file_bytes = await file.read()
    text = extract_text_from_pdf(file_bytes)
    result = ingest_document(text, document_name=file.filename, user_id=user_id)
    return result


class RagQuestionRequest(BaseModel):
    question: str
    user_id: str = "harsh"

@router.post("/rag/ask")
async def rag_ask_endpoint(request: RagQuestionRequest):
    result = answer_from_documents(request.question, request.user_id)
    return result

from agents.dsa_coach.agent import coach_on_topic

class DsaCoachRequest(BaseModel):
    weak_topic: str

@router.post("/dsa/coach")
async def dsa_coach_endpoint(request: DsaCoachRequest):
    result = coach_on_topic(request.weak_topic)
    return result

from memory.session_manager import create_session
from agents.interviewer.agent import start_interview, continue_interview

class StartInterviewRequest(BaseModel):
    topic: str

@router.post("/interview/start")
async def start_interview_endpoint(request: StartInterviewRequest):
    session_id = create_session()
    question = start_interview(session_id, request.topic)
    return {"session_id": session_id, "message": question}


class ContinueInterviewRequest(BaseModel):
    session_id: str
    answer: str

@router.post("/interview/continue")
async def continue_interview_endpoint(request: ContinueInterviewRequest):
    response = continue_interview(request.session_id, request.answer)
    return {"session_id": request.session_id, "message": response}

from agents.feedback.agent import generate_feedback

@router.get("/interview/feedback/{session_id}")
async def feedback_endpoint(session_id: str):
    feedback = generate_feedback(session_id)
    return feedback
