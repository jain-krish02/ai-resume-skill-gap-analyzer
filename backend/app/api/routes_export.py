from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any, List
from app.modules.pdf_generator import PDFGenerator
import os

router = APIRouter()
pdf_gen = PDFGenerator()

class ExportRequest(BaseModel):
    target_role: str
    match_score: float
    missing_must_have: List[Dict[str, Any]]
    missing_good_to_have: List[Dict[str, Any]]
    overlapping: List[Dict[str, Any]]
    roadmap: List[Dict[str, Any]]

@router.post("/")
def export_pdf(request: ExportRequest):
    try:
        data_dict = request.model_dump()
        pdf_path = pdf_gen.generate_report(data_dict)
        return FileResponse(
            path=pdf_path, 
            filename="AI_Skill_Gap_Report.pdf", 
            media_type="application/pdf",
            background=None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")
