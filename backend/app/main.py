from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_upload import router as upload_router
from app.api.routes_extract import router as extract_router
from app.api.routes_job import router as job_router
from app.api.routes_gap import router as gap_router
from app.api.routes_roadmap import router as roadmap_router
from app.api.routes_export import router as export_router

app = FastAPI(
    title="AI Resume Skill Gap Analyzer",
    description="API for comparing resumes to job descriptions and generating learning roadmaps.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload_router, prefix="/api/upload", tags=["Upload"])
app.include_router(extract_router, prefix="/api/extract", tags=["Extract"])
app.include_router(job_router, prefix="/api/job", tags=["Job"])
app.include_router(gap_router, prefix="/api/gap", tags=["Gap"])
app.include_router(roadmap_router, prefix="/api/roadmap", tags=["Roadmap"])
app.include_router(export_router, prefix="/api/export", tags=["Export"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Resume Skill Gap Analyzer API"}
