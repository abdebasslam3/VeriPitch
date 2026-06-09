from fastapi import APIRouter, Depends, HTTPException, Form
from core.api.proposals import generate_proposal_with_gemini, generate_proposal_with_claude
from core.utils.encryption import decrypt_api_key
from supabase import create_client, Client
import os
import json

router = APIRouter(prefix="/api/v1")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@router.post("/generate-proposal")
async def generate_proposal_endpoint(
    whop_user_id: str = Form(...), # Verified from session in production
    job_description: str = Form(...),
    screening_questions: str = Form(""),
    model_choice: str = Form(...),
    encrypted_api_key: str = Form(...),
    dynamic_salt: str = Form(...)
):
    # 1. Fetch REAL profile from Supabase (Truth Source)
    user_res = supabase.table("users").select("id, subscription_status").eq("whop_user_id", whop_user_id).single().execute()
    if not user_res.data or user_res.data.get("subscription_status") != "active":
        raise HTTPException(status_code=403, detail="Subscription inactive")

    user_uuid = user_res.data["id"]
    profile_res = supabase.table("profiles").select("*").eq("user_id", user_uuid).single().execute()

    if not profile_res.data:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile_data = profile_res.data

    # 2. Decrypt API Key
    try:
        api_key = decrypt_api_key(encrypted_api_key, dynamic_salt)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid API Key or Salt")

    # 3. Generate Proposal using Truth Data
    if model_choice == "gemini":
        result = generate_proposal_with_gemini(api_key, job_description, profile_data, screening_questions)
    else:
        result = generate_proposal_with_claude(api_key, job_description, profile_data, screening_questions)

    return {"proposal": result}

@router.post("/check-cooldown")
async def check_cooldown(whop_user_id: str = Form(...), skill_name: str = Form(...)):
    user_res = supabase.table("users").select("id").eq("whop_user_id", whop_user_id).single().execute()
    user_uuid = user_res.data["id"]

    # Check for active cooldown in DB
    from datetime import datetime, timezone
    cooldown_res = supabase.table("quiz_cooldowns")\
        .select("locked_until")\
        .eq("user_id", user_uuid)\
        .eq("skill_name", skill_name)\
        .gt("locked_until", datetime.now(timezone.utc).isoformat())\
        .execute()

    if cooldown_res.data:
        return {"locked": True, "until": cooldown_res.data[0]["locked_until"]}
    return {"locked": False}
