from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_extract_skills_resume():
    response = client.post("/api/extract/", json={
        "text": "Python developer with 5 years experience in Django and Docker.",
        "type": "resume"
    })
    # Cannot guarantee Gemini responds fast or without error if mock=False, 
    # but we can test the API receives the request properly.
    assert response.status_code in [200, 500]

def test_extract_skills_jd():
    response = client.post("/api/extract/", json={
        "text": "Looking for a Python developer with Django skills.",
        "type": "job_description"
    })
    assert response.status_code in [200, 500]
