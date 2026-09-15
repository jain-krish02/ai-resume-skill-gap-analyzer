import json
import logging
from google import genai
from google.genai import types
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Initialize the client
client = genai.Client(api_key="AQ.Ab8RN6JqZlNtEwcQlatKp3mbnlgA6Lso7KOPmMQPKQFJGg61og")

class SkillExtractor:
    """Handles structured skill extraction from parsed resume/job description text."""
    
    def __init__(self, use_mock: bool = False):
        self.use_mock = use_mock
        
    async def extract_skills(self, raw_text: str, is_job_description: bool = False) -> Dict[str, Any]:
        """Extracts skills, tools, and experience from raw text using Gemini."""
        if not raw_text or not raw_text.strip():
            raise ValueError("Text content is empty.")
            
        logger.info("Initiating skill extraction process with Gemini...")
        
        if self.use_mock:
            return self._mock_extraction(raw_text)
            
        return await self._gemini_extraction(raw_text, is_job_description)
        
    async def _gemini_extraction(self, text: str, is_job_description: bool) -> Dict[str, Any]:
        if is_job_description:
            prompt = f"""
            You are an expert HR parser. Extract the required skills, tools, and educational qualifications from the following Job Description.
            Return a JSON object with this EXACT structure (no markdown, just JSON):
            {{
                "required_skills": [
                    {{"skill_name": "Python", "category": "Technical", "priority": "Must-Have", "weight": 1.0}},
                    {{"skill_name": "Docker", "category": "Tool", "priority": "Good-to-Have", "weight": 0.5}}
                ]
            }}
            
            Job Description:
            {text}
            """
        else:
            prompt = f"""
            You are an expert HR parser. Extract the skills, tools, experience years, and education from the following Resume.
            Return a JSON object with this EXACT structure (no markdown, just JSON):
            {{
                "skills": [
                    {{"name": "Python", "category": "Technical"}},
                    {{"name": "Communication", "category": "Soft Skill"}}
                ],
                "tools": [
                    {{"name": "Git", "category": "Tool"}}
                ],
                "education": ["B.Tech Computer Science"],
                "experience_years": 2
            }}
            
            Resume Text:
            {text}
            """
            
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                )
            )
            return json.loads(response.text)
        except Exception as e:
            logger.error(f"Gemini API Error: {str(e)}")
            raise ValueError(f"AI Extraction failed: {str(e)}")

    def _mock_extraction(self, text: str) -> Dict[str, Any]:
        # Existing mock fallback...
        text_lower = text.lower()
        skills_found = []
        tools_found = []
        mock_skills = ["python", "java", "javascript", "react", "machine learning", "data analysis", "sql"]
        mock_tools = ["git", "docker", "aws", "excel", "tableau"]
        for skill in mock_skills:
            if skill in text_lower:
                skills_found.append({"name": skill.title(), "category": "Technical"})
        for tool in mock_tools:
            if tool in text_lower:
                tools_found.append({"name": tool.title(), "category": "Tool"})
        return {
            "skills": skills_found,
            "tools": tools_found,
            "education": ["Mock Education"],
            "experience_years": 2
        }
