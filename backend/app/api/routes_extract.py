from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.modules.skill_extractor import SkillExtractor
from app.modules.validation import sanitize_job_description

router = APIRouter()
extractor = SkillExtractor(use_mock=False)

class ExtractRequest(BaseModel):
    text: str
    type: str  # "resume" or "job_description"

@router.post("/")
async def extract_skills(request: ExtractRequest):
    try:
        sanitized_text = sanitize_job_description(request.text)
        profile = await extractor.extract_skills(sanitized_text)
        return {
            "status": "success",
            "data": profile
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
