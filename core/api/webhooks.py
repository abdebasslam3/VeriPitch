from fastapi import APIRouter, Request, HTTPException
import os
import hashlib
import hmac
from supabase import create_client, Client

router = APIRouter()

WHOP_WEBHOOK_SECRET = os.getenv("WHOP_WEBHOOK_SECRET")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@router.post("/api/webhooks/whop")
async def whop_webhook(request: Request):
    signature = request.headers.get("x-whop-signature")
    if not signature:
        raise HTTPException(status_code=401, detail="Missing signature")

    body = await request.body()

    # Secure HMAC verification
    expected_signature = hmac.new(
        WHOP_WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    data = await request.json()
    event = data.get("event")

    if event in ["membership.went_inactive", "membership.cancelled"]:
        whop_user_id = data.get("data", {}).get("user_id")
        # Update user status to cancelled in Supabase
        supabase.table("users").update({"subscription_status": "cancelled"}).eq("whop_user_id", whop_user_id).execute()

    return {"status": "ok"}
