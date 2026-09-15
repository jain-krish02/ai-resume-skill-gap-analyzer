from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
import uuid

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(120))
    email = Column(String(150), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Resume(Base):
    __tablename__ = "resumes"
    resume_id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=True) # allow anonymous for now
    file_name = Column(String(255))
    file_type = Column(String(10))
    raw_text = Column(Text)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

class Skill(Base):
    __tablename__ = "skills"
    skill_id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(100), unique=True, index=True)
    category = Column(String(50))

class JobRole(Base):
    __tablename__ = "job_roles"
    role_id = Column(String, primary_key=True, default=generate_uuid)
    role_title = Column(String(150))
    is_custom = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class JobRoleSkill(Base):
    __tablename__ = "job_role_skills"
    role_skill_id = Column(String, primary_key=True, default=generate_uuid)
    role_id = Column(String, ForeignKey("job_roles.role_id"))
    skill_id = Column(String, ForeignKey("skills.skill_id"))
    priority = Column(String) # 'Must-Have' or 'Good-to-Have'
    weight = Column(Float, default=1.0)
    
    role = relationship("JobRole", backref="required_skills")
    skill = relationship("Skill")

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
