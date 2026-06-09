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

@router.post("/check-api-key")
async def check_api_key(
    encrypted_api_key: str = Form(...),
    dynamic_salt: str = Form(...),
    model_choice: str = Form(...)
):
    """Lighweight ping to verify API key validity."""
    try:
        api_key = decrypt_api_key(encrypted_api_key, dynamic_salt)
        if model_choice == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            # Very lightweight call
            genai.get_model('models/gemini-1.5-flash')
        else:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            # Claude doesn't have a simple ping, but we can try a tiny message
            pass
        return {"status": "valid"}
    except Exception:
        return {"status": "invalid"}

@router.post("/generate-proposal")
async def generate_proposal_endpoint(
    whop_user_id: str = Form(...),
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
    # 2.5 Calculate Market Fit Score
    from core.matcher import SkillMatcher
    user_skills = [s["name"] for s in profile_data.get("skills", [])]
    matcher = SkillMatcher(user_skills)
    report = matcher.analyze_job(job_description)

    market_fit_score = 0
    if report["required_all"]:
        market_fit_score = int((len(report["matched"]) / len(report["required_all"])) * 100)

    # 3. Generate Proposal using Truth Data
    if model_choice == "gemini":
        result = generate_proposal_with_gemini(api_key, job_description, profile_data, screening_questions)
    else:
        result = generate_proposal_with_claude(api_key, job_description, profile_data, screening_questions)

    # 4. Log to history
    supabase.table("proposals_history").insert({
        "user_id": user_uuid,
        "job_title": "Job Analysis",
        "job_description": job_description,
        "generated_proposal": result,
        "used_model": model_choice,
        "market_fit_score": market_fit_score
    }).execute()

    return {
        "proposal": result,
        "market_fit_score": market_fit_score,
        "match_report": report
    }

from fastapi import UploadFile, File

@router.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    encrypted_api_key: str = Form(...),
    dynamic_salt: str = Form(...),
    whop_user_id: str = Form(...)
):
    from core.api.profile import extract_text_from_pdf, parse_profile_with_ai

    # 1. Decrypt API Key to use for parsing
    api_key = decrypt_api_key(encrypted_api_key, dynamic_salt)

    # 2. Extract Text
    content = await file.read()
    text = extract_text_from_pdf(content)

    # 3. Parse with AI
    profile_json = parse_profile_with_ai(text, api_key)

    if profile_json:
        # 4. Save to Supabase
        user_res = supabase.table("users").select("id").eq("whop_user_id", whop_user_id).single().execute()
        user_uuid = user_res.data["id"]

        supabase.table("profiles").update({
            "bio_summary": profile_json.get("bio_summary"),
            "skills": profile_json.get("skills"),
            "portfolio": profile_json.get("portfolio")
        }).eq("user_id", user_uuid).execute()

        return {"status": "success", "profile": profile_json}

    return {"status": "error", "message": "Failed to parse resume"}

@router.post("/ingest-text-profile")
async def ingest_text_profile(
    profile_text: str = Form(...),
    encrypted_api_key: str = Form(...),
    dynamic_salt: str = Form(...),
    whop_user_id: str = Form(...)
):
    from core.api.profile import parse_profile_with_ai
    api_key = decrypt_api_key(encrypted_api_key, dynamic_salt)
    profile_json = parse_profile_with_ai(profile_text, api_key)

    if profile_json:
        user_res = supabase.table("users").select("id").eq("whop_user_id", whop_user_id).single().execute()
        user_uuid = user_res.data["id"]
        supabase.table("profiles").update(profile_json).eq("user_id", user_uuid).execute()
        return {"status": "success", "profile": profile_json}
    return {"status": "error"}

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

@router.post("/start-smart-quiz")
async def start_smart_quiz(
    whop_user_id: str = Form(...),
    skill_name: str = Form(...),
    encrypted_api_key: str = Form(...),
    dynamic_salt: str = Form(...)
):
    # 1. Check Cooldown
    status = await check_cooldown(whop_user_id, skill_name)
    if status.get("locked"):
        return {"status": "locked", "until": status.get("until")}

    # 2. Generate MCQ via AI
    from core.api.proposals import generate_mcq
    api_key = decrypt_api_key(encrypted_api_key, dynamic_salt)

    user_res = supabase.table("users").select("id").eq("whop_user_id", whop_user_id).single().execute()
    user_uuid = user_res.data["id"]
    profile_res = supabase.table("profiles").select("bio_summary").eq("user_id", user_uuid).single().execute()

    quiz = generate_mcq(skill_name, profile_res.data.get("bio_summary", ""), api_key)
    return {"status": "success", "quiz": quiz}

@router.post("/verify-quiz-answer")
async def verify_quiz_answer(
    whop_user_id: str = Form(...),
    skill_name: str = Form(...),
    is_correct: bool = Form(...),
    encrypted_api_key: str = Form(...),
    dynamic_salt: str = Form(...)
):
    user_res = supabase.table("users").select("id").eq("whop_user_id", whop_user_id).single().execute()
    user_uuid = user_res.data["id"]

    if is_correct:
        # Update skill to verified in JSONB
        profile_res = supabase.table("profiles").select("skills").eq("user_id", user_uuid).single().execute()
        skills = profile_res.data.get("skills", [])
        for skill in skills:
            if skill["name"].lower() == skill_name.lower():
                skill["verified"] = True
                skill["source"] = "quiz"

        supabase.table("profiles").update({"skills": skills}).eq("user_id", user_uuid).execute()
        return {"status": "success", "message": "Skill verified!"}
    else:
        # Set 2-hour cooldown
        from datetime import datetime, timedelta, timezone
        locked_until = (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat()
        supabase.table("quiz_cooldowns").upsert({
            "user_id": user_uuid,
            "skill_name": skill_name,
            "locked_until": locked_until
        }).execute()
        return {"status": "failed", "locked_until": locked_until}
