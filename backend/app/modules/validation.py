from fastapi import HTTPException, UploadFile
import os

def validate_resume_file(file: UploadFile):
    allowed_extensions = {".pdf", ".docx"}
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported file format '{ext}'. Only PDF and DOCX are allowed.")
    
    return True

def sanitize_job_description(text: str) -> str:
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")
    
    # Basic sanitization
    sanitized = text.strip()
    if len(sanitized) > 10000:
        raise HTTPException(status_code=400, detail="Job description is too long.")
        
    return sanitized
