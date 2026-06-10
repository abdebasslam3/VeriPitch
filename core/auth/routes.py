from fastapi import APIRouter, Depends, HTTPException, Query
from core.auth.whop import exchange_code_for_token, get_whop_user, validate_user_subscription
from core.utils.encryption import generate_dynamic_salt
import os

router = APIRouter(prefix="/api/v1/auth")

from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@router.get("/callback")
async def whop_callback(code: str):
    # 1. Exchange code
    token_data = await exchange_code_for_token(code)
    access_token = token_data.get("access_token")

    # 2. Get User Info
    user_data = await get_whop_user(access_token)
    whop_user_id = user_data.get("id")
    email = user_data.get("email")
    memberships = user_data.get("memberships", [])

    # 3. Validate Plan
    is_valid = await validate_user_subscription(memberships)
    if not is_valid:
        raise HTTPException(
            status_code=403,
            detail="عذراً، اشتراكك الحالي لا يمنحك صلاحية الوصول لهذه المنصة"
        )

    # 4. Sync with Supabase
    # Check if user exists
    user_res = supabase.table("users").select("*").eq("whop_user_id", whop_user_id).execute()

    if not user_res.data:
        # Create new user
        new_user = {
            "whop_user_id": whop_user_id,
            "email": email,
            "subscription_status": "active"
        }
        # Let Supabase generate the UUID
        res = supabase.table("users").insert(new_user).execute()

        if res.data:
            user_uuid = res.data[0]["id"]
            # Initialize profile
            supabase.table("profiles").insert({"user_id": user_uuid}).execute()
    else:
        # Update status
        supabase.table("users").update({"subscription_status": "active"}).eq("whop_user_id", whop_user_id).execute()

    # 5. Generate Session / Dynamic Salt
    dynamic_salt = generate_dynamic_salt()

    return {
        "status": "success",
        "whop_user_id": whop_user_id,
        "dynamic_salt": dynamic_salt,
        "email": email
    }
