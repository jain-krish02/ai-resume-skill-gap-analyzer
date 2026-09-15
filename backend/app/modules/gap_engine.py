from typing import List, Dict, Any

class GapAnalysisEngine:
    """Computes similarity score and categorizes missing skills."""
    
    def __init__(self):
        pass
        
    def compare_skills(self, candidate_skills: List[Dict[str, str]], required_skills: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        candidate_skills: [{"name": "Python", "category": "Technical"}, ...]
        required_skills: [{"skill_name": "Python", "priority": "Must-Have", "weight": 1.0}, ...]
        """
        
        candidate_skill_names = {s["name"].lower() for s in candidate_skills}
        
        overlapping = []
        missing_must_have = []
        missing_good_to_have = []
        
        total_weight = 0.0
        earned_weight = 0.0
        
        for req in required_skills:
            req_name = req["skill_name"].lower()
            weight = req.get("weight", 1.0)
            priority = req.get("priority", "Must-Have")
            
            total_weight += weight
            
            if req_name in candidate_skill_names:
                earned_weight += weight
                overlapping.append(req)
            else:
                if priority == "Must-Have":
                    missing_must_have.append(req)
                else:
                    missing_good_to_have.append(req)
                    
        # Compute match score (0 to 100)
        match_score = (earned_weight / total_weight * 100) if total_weight > 0 else 100.0
        
        return {
            "match_score": round(match_score, 2),
            "overlapping": overlapping,
            "missing_must_have": missing_must_have,
            "missing_good_to_have": missing_good_to_have
        }
