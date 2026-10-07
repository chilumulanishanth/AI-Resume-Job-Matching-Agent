from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from app.services.parser import extract_text
from app.services.matcher import match_resume_to_job
from app.services.llm import generate_ai_analysis

app = FastAPI(
    title="AI Resume & Job Matching Agent",
    version="1.0.0",
    description="Resume parsing, skill matching, retrieval and optional LLM analysis API."
)

class JobMatchRequest(BaseModel):
    resume_text: str
    job_description: str

@app.get("/health")
def health():
    return {"status": "ok", "service": "ai-resume-job-matching-agent"}

@app.post("/match")
def match_text(payload: JobMatchRequest):
    if not payload.resume_text.strip() or not payload.job_description.strip():
        raise HTTPException(status_code=400, detail="Resume text and job description are required.")
    result = match_resume_to_job(payload.resume_text, payload.job_description)
    result["ai_analysis"] = generate_ai_analysis(payload.resume_text, payload.job_description, result)
    return result

@app.post("/match-file")
async def match_file(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required.")
    try:
        content = await resume.read()
        resume_text = extract_text(resume.filename or "", content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    result = match_resume_to_job(resume_text, job_description)
    result["ai_analysis"] = generate_ai_analysis(resume_text, job_description, result)
    return result
