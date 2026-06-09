from fastapi import APIRouter, Depends, HTTPException, Query
from core.auth.whop import exchange_code_for_token, get_whop_user, validate_user_subscription
from core.utils.encryption import generate_dynamic_salt
import os

router = APIRouter(prefix="/api/auth")

from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@router.get("/whop/callback")
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
        # Create new user in auth.users is complex via service role without password,
        # so we rely on the whop_user_id as the primary identifier in our custom users table.
        # For MVP, we'll ensure they exist in our 'users' table.
        # Note: In a real Supabase Auth setup, you'd use their Auth API.
        new_user = {
            "id": str(os.urandom(16).hex()), # Placeholder UUID if not using Supabase Auth fully
            "whop_user_id": whop_user_id,
            "email": email,
            "subscription_status": "active"
        }
        # In production, 'id' should be a real UUID linked to auth.users if possible
        # For now we use a workaround to satisfy the schema or modify schema to allow non-auth users
        supabase.table("users").insert(new_user).execute()

        # Initialize profile
        supabase.table("profiles").insert({"user_id": new_user["id"]}).execute()
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
