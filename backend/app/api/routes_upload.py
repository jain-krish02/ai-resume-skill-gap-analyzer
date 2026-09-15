from fastapi import APIRouter, UploadFile, File, HTTPException
from app.modules.validation import validate_resume_file
from app.modules.parser import ResumeParser
import io

router = APIRouter()

@router.post("/")
async def upload_resume(file: UploadFile = File(...)):
    try:
        validate_resume_file(file)
        
        content = await file.read()
        
        parser = ResumeParser(content, file.filename)
        parsed_data = parser.parse()
        
        return {
            "status": "success",
            "message": "Resume uploaded and parsed successfully.",
            "data": parsed_data
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
