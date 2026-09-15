from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db, JobRole

router = APIRouter()

@router.get("/")
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(JobRole).filter(JobRole.is_custom == False).all()
    return {
        "status": "success",
        "data": [{"role_id": r.role_id, "role_title": r.role_title} for r in roles]
    }

@router.get("/{role_id}/skills")
def get_role_skills(role_id: str, db: Session = Depends(get_db)):
    role = db.query(JobRole).filter(JobRole.role_id == role_id).first()
    if not role:
        return {"status": "error", "message": "Role not found"}
        
    skills = []
    for rs in role.required_skills:
        skills.append({
            "skill_name": rs.skill.name,
            "category": rs.skill.category,
            "priority": rs.priority,
            "weight": rs.weight
        })
        
    return {
        "status": "success",
        "data": {
            "role_title": role.role_title,
            "required_skills": skills
        }
    }
