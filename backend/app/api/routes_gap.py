from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models.database import get_db, JobRole
from app.modules.gap_engine import GapAnalysisEngine
from typing import List, Dict, Any, Optional

router = APIRouter()
engine = GapAnalysisEngine()

class GapRequest(BaseModel):
    candidate_skills: List[Dict[str, Any]]
    target_role_id: str
    custom_requirements: Optional[List[Dict[str, Any]]] = None

@router.post("/")
def analyze_gap(request: GapRequest, db: Session = Depends(get_db)):
    print("=== DEBUG GAP API ===")
    print("Candidate skills count:", len(request.candidate_skills))
    print("Candidate skills names:", [s.get("name") for s in request.candidate_skills])
    print("=======================")
    
    if request.target_role_id == "custom" and request.custom_requirements is not None:
        required_skills = request.custom_requirements
    else:
        role = db.query(JobRole).filter(JobRole.role_id == request.target_role_id).first()
        if not role:
            raise HTTPException(status_code=404, detail="Target role not found.")
            
        required_skills = []
        for rs in role.required_skills:
            required_skills.append({
                "skill_name": rs.skill.name,
                "category": rs.skill.category,
                "priority": rs.priority,
                "weight": rs.weight
            })
        
    gap_report = engine.compare_skills(request.candidate_skills, required_skills)

    
    return {
        "status": "success",
        "data": gap_report
    }
