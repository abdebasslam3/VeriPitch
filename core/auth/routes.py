from fastapi import APIRouter, Depends, HTTPException, Query
from core.auth.whop import exchange_code_for_token, get_whop_user, validate_user_subscription
from core.utils.encryption import generate_dynamic_salt
import os

router = APIRouter(prefix="/api/auth")

@router.get("/whop/callback")
async def whop_callback(code: str):
    # 1. Exchange code
    token_data = await exchange_code_for_token(code)
    access_token = token_data.get("access_token")

    # 2. Get User Info
    user_data = await get_whop_user(access_token)
    memberships = user_data.get("memberships", [])

    # 3. Validate Plan
    is_valid = await validate_user_subscription(memberships)
    if not is_valid:
        raise HTTPException(
            status_code=403,
            detail="عذراً، اشتراكك الحالي لا يمنحك صلاحية الوصول لهذه المنصة"
        )

    # 4. Generate Session / Dynamic Salt
    dynamic_salt = generate_dynamic_salt()

    # 5. TODO: Sync with Supabase and set Secure Cookie
    return {
        "status": "success",
        "user": user_data.get("id"),
        "dynamic_salt": dynamic_salt
    }
