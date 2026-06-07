from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from core.matcher import SkillMatcher
from core.whop_client import WhopClient
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="VeriPitch API")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your domain
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
whop_client = WhopClient()

class JobAnalysisRequest(BaseModel):
    freelancer_skills: List[str]
    job_description: str

@app.get("/")
async def root():
    return {"message": "Welcome to VeriPitch API"}

@app.post("/analyze")
async def analyze_job(request: JobAnalysisRequest):
    """
    Endpoint to analyze a job description against freelancer skills.
    """
    try:
        matcher = SkillMatcher(request.freelancer_skills)
        result = matcher.analyze_job(request.job_description)
        # Here we could call an LLM to generate a more complex proposal
        # based on the matched skills.
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/verify-access/{user_id}")
async def verify_access(user_id: str, product_id: str):
    """
    Endpoint to verify if a user has access to a specific product via Whop.
    """
    has_access = whop_client.validate_access(user_id, product_id)
    return {"user_id": user_id, "has_access": has_access}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
