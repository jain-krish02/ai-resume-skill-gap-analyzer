from app.models.database import SessionLocal, JobRole, Skill, JobRoleSkill

def seed_database():
    db = SessionLocal()
    
    # Check if roles already exist
    if db.query(JobRole).count() > 0:
        db.close()
        return

    # Seed Skills
    skills_data = [
        {"name": "Python", "category": "Technical"},
        {"name": "Java", "category": "Technical"},
        {"name": "Javascript", "category": "Technical"},
        {"name": "React", "category": "Technical"},
        {"name": "Sql", "category": "Technical"},
        {"name": "Machine Learning", "category": "Technical"},
        {"name": "Data Analysis", "category": "Technical"},
        {"name": "Git", "category": "Tool"},
        {"name": "Docker", "category": "Tool"}
    ]
    
    skill_objects = {}
    for s in skills_data:
        skill = Skill(**s)
        db.add(skill)
        skill_objects[s["name"].lower()] = skill
    db.commit()
    
    # Seed Job Roles
    roles = [
        {"title": "Software Engineer", "skills": [("python", "Must-Have"), ("java", "Good-to-Have"), ("git", "Must-Have"), ("docker", "Good-to-Have")]},
        {"title": "Data Analyst", "skills": [("python", "Must-Have"), ("sql", "Must-Have"), ("data analysis", "Must-Have"), ("tableau", "Good-to-Have")]},
        {"title": "Frontend Developer", "skills": [("javascript", "Must-Have"), ("react", "Must-Have"), ("git", "Must-Have")]}
    ]
    
    for r in roles:
        role = JobRole(role_title=r["title"], is_custom=False)
        db.add(role)
        db.commit()
        db.refresh(role)
        
        for skill_name, priority in r["skills"]:
            if skill_name in skill_objects:
                jrs = JobRoleSkill(role_id=role.role_id, skill_id=skill_objects[skill_name].skill_id, priority=priority, weight=1.0 if priority == "Must-Have" else 0.5)
                db.add(jrs)
                
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_database()
    print("Database seeded successfully.")
