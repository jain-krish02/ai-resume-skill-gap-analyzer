import re
from typing import List, Dict, Any
from difflib import SequenceMatcher

class GapAnalysisEngine:
    """Computes similarity score and categorizes missing skills."""
    
    def __init__(self):
        pass
        
    def _is_match(self, req: str, cand: str) -> bool:
        req = req.lower().strip()
        cand = cand.lower().strip()
        
        if req == cand:
            return True
            
        # Check if req is a whole word inside cand, or vice versa
        # (useful if LLM clumped skills together like "Git, GitHub")
        try:
            if re.search(r'\b' + re.escape(req) + r'\b', cand):
                return True
            if re.search(r'\b' + re.escape(cand) + r'\b', req):
                return True
        except:
            pass
            
        # Fuzzy match for slight variations (OOP vs OOPs, etc.)
        if SequenceMatcher(None, req, cand).ratio() > 0.85:
            return True
            
        # Handling specific common tech equivalents or abbreviations
        # Degrees
        if ('bachelor' in req or 'b.tech' in req or 'bs ' in req or 'b.s' in req) and \
           ('bachelor' in cand or 'b.tech' in cand or 'bs ' in cand or 'b.s' in cand):
           if 'computer science' in req and 'computer science' in cand:
               return True
               
        # Word subset matching (e.g. "Data Structures and Algorithms" vs "Data Structures & Algorithms (DSA)")
        req_words = set(w for w in re.sub(r'[^a-z0-9\s]', ' ', req.replace('and', ' ')).split() if len(w) > 1)
        cand_words = set(w for w in re.sub(r'[^a-z0-9\s]', ' ', cand.replace('and', ' ')).split() if len(w) > 1)
        
        if req_words and cand_words:
            if req_words.issubset(cand_words) or cand_words.issubset(req_words):
                return True
                    
        return False
        
    def compare_skills(self, candidate_skills: List[Dict[str, str]], required_skills: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        candidate_skills: [{"name": "Python", "category": "Technical"}, ...]
        required_skills: [{"skill_name": "Python", "priority": "Must-Have", "weight": 1.0}, ...]
        """
        
        candidate_skill_names = [s.get("name", "") for s in candidate_skills]
        
        overlapping = []
        missing_must_have = []
        missing_good_to_have = []
        
        total_weight = 0.0
        earned_weight = 0.0
        
        for req in required_skills:
            req_name = req.get("skill_name", "")
            weight = req.get("weight", 1.0)
            priority = req.get("priority", "Must-Have")
            
            total_weight += weight
            
            # Check if this required skill matches any candidate skill
            matched = False
            for cand_name in candidate_skill_names:
                if self._is_match(req_name, cand_name):
                    matched = True
                    break
            
            if matched:
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
