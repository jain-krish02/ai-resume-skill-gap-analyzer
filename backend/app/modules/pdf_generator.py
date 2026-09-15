import os
import tempfile
import logging
from typing import Dict, Any

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

logger = logging.getLogger(__name__)

class PDFGenerator:
    """Generates PDF reports from analysis results using ReportLab."""
    
    def generate_report(self, analysis_data: Dict[str, Any]) -> str:
        """
        Generates a PDF and returns the file path.
        """
        fd, path = tempfile.mkstemp(suffix=".pdf")
        os.close(fd)
        
        doc = SimpleDocTemplate(path, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Custom Styles
        title_style = styles['Title']
        title_style.textColor = colors.HexColor('#2563eb')
        
        h2_style = styles['Heading2']
        h2_style.textColor = colors.HexColor('#1e40af')
        
        normal_style = styles['Normal']
        
        story = []
        
        # Title
        story.append(Paragraph("AI Resume Skill Gap Analyzer Report", title_style))
        story.append(Spacer(1, 20))
        
        # Summary
        target_role = analysis_data.get('target_role', 'Custom Role')
        match_score = analysis_data.get('match_score', 0)
        
        story.append(Paragraph(f"<b>Target Role:</b> {target_role}", normal_style))
        story.append(Paragraph(f"<b>Match Score:</b> <font color='green'>{match_score}%</font>", normal_style))
        story.append(Spacer(1, 20))
        
        # Missing Critical
        story.append(Paragraph("Missing Critical Skills (Must-Have)", h2_style))
        missing_must = [s['skill_name'] for s in analysis_data.get('missing_must_have', [])]
        if missing_must:
            story.append(Paragraph(", ".join(missing_must), normal_style))
        else:
            story.append(Paragraph("None! You have all critical skills.", normal_style))
        story.append(Spacer(1, 15))
        
        # Missing Good to Have
        story.append(Paragraph("Missing Good-to-Have Skills", h2_style))
        missing_good = [s['skill_name'] for s in analysis_data.get('missing_good_to_have', [])]
        if missing_good:
            story.append(Paragraph(", ".join(missing_good), normal_style))
        else:
            story.append(Paragraph("None missing.", normal_style))
        story.append(Spacer(1, 15))
        
        # Overlapping
        story.append(Paragraph("Matching Skills", h2_style))
        matching = [s['skill_name'] for s in analysis_data.get('overlapping', [])]
        if matching:
            story.append(Paragraph(", ".join(matching), normal_style))
        else:
            story.append(Paragraph("No exact matches found.", normal_style))
        story.append(Spacer(1, 20))
        
        # Roadmap
        story.append(Paragraph("Learning Roadmap & Recommendations", h2_style))
        story.append(Spacer(1, 10))
        
        for step in analysis_data.get('roadmap', []):
            story.append(Paragraph(f"<b>Week {step['week']}: Learn {step['skill']}</b>", normal_style))
            story.append(Paragraph(f"<i>{step['description']}</i>", normal_style))
            
            # Projects
            story.append(Spacer(1, 5))
            story.append(Paragraph("<b>Projects:</b>", normal_style))
            for proj in step.get('projects', []):
                story.append(Paragraph(f"- {proj}", normal_style))
                
            # Courses
            story.append(Spacer(1, 5))
            story.append(Paragraph("<b>Courses:</b>", normal_style))
            for course in step.get('courses', []):
                story.append(Paragraph(f"- <a href='{course['url']}' color='blue'>{course['title']}</a> ({course['platform']})", normal_style))
            
            story.append(Spacer(1, 15))
            
        doc.build(story)
        return path
