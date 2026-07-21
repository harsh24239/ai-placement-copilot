from fastapi import APIRouter, UploadFile, File, HTTPException
from tools.pdf_reader import extract_text_from_pdf

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