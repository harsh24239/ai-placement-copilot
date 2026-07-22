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
