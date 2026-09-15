from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from app.modules.recommender import RoadmapRecommender

router = APIRouter()
recommender = RoadmapRecommender()

class RoadmapRequest(BaseModel):
    missing_must_have: List[Dict[str, Any]]
    missing_good_to_have: List[Dict[str, Any]]

@router.post("/")
def generate_roadmap(request: RoadmapRequest):
    roadmap = recommender.generate_roadmap(request.missing_must_have, request.missing_good_to_have)
    
    return {
        "status": "success",
        "data": roadmap
    }
