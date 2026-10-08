import os
import json
import re
import logging
from dotenv import load_dotenv
from groq import Groq
from typing import List, Dict, Any

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

logger = logging.getLogger(__name__)

class RoadmapRecommender:
    """Generates learning roadmaps, projects, and courses for missing skills using Gemini."""
    
    def generate_roadmap(self, missing_must_have: List[Dict[str, Any]], missing_good_to_have: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generates a week-wise roadmap based on missing skills via LLM."""
        
        all_missing = missing_must_have + missing_good_to_have
        if not all_missing:
            return []
            
        skill_names = [s["skill_name"] for s in all_missing]
        
        prompt = f"""
        You are an expert career coach and EdTech planner. 
        Create a week-by-week learning roadmap for a student to learn the following missing skills: {", ".join(skill_names)}.
        
        For each skill, provide:
        1. "week": An integer representing the sequence (start from 1, group foundational skills early).
        2. "skill": The name of the skill.
        3. "description": A short explanation of what to focus on.
        4. "priority": "Must-Have" or "Good-to-Have" (Maintain this original priority).
        5. "projects": A list of 2-3 CONCRETE, specific mini-project ideas (do NOT use generic 'Build a basic app', instead say things like 'Build a REST API for a bookstore using FastAPI').
        6. "courses": A list of 1-2 recommended popular courses on platforms like Coursera or Udemy. Use format {{"title": "Course Name", "platform": "Platform Name", "url": "https://www.udemy.com/courses/search/?q=url+encoded+course+name"}}.
        
        Return a JSON array of objects.
        """
        
        try:
            logger.info("Calling Groq for roadmap generation...")
            response = client.chat.completions.create(
                model='openai/gpt-oss-120b',
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.choices[0].message.content
            # Extremely robust JSON extraction
            match = re.search(r'```(?:json)?(.*?)```', content, re.DOTALL)
            if match:
                content = match.group(1).strip()
            
            start_brace = content.find('{')
            start_bracket = content.find('[')
            start = -1
            if start_brace != -1 and start_bracket != -1:
                start = min(start_brace, start_bracket)
            else:
                start = max(start_brace, start_bracket)
                
            end_brace = content.rfind('}')
            end_bracket = content.rfind(']')
            end = max(end_brace, end_bracket)
            
            if start != -1 and end != -1:
                content = content[start:end+1]
                
            return json.loads(content)
        except Exception as e:
            logger.error(f"Gemini API Error in recommender: {str(e)}")
            # Fallback mock if LLM fails
            return self._fallback_roadmap(all_missing)
            
    def _fallback_roadmap(self, missing_skills) -> List[Dict[str, Any]]:
        roadmap = []
        for i, skill in enumerate(missing_skills):
            roadmap.append({
                "week": i + 1,
                "skill": skill["skill_name"],
                "description": f"Learn the basics of {skill['skill_name']}.",
                "priority": skill.get("priority", "Good-to-Have"),
                "projects": [f"Create a mini-project focusing on {skill['skill_name']} core features."],
                "courses": [{"title": f"Intro to {skill['skill_name']}", "platform": "YouTube", "url": f"https://www.youtube.com/results?search_query={skill['skill_name']}"}]
            })
        return roadmap
