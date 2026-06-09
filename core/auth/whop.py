import httpx
import os
from fastapi import HTTPException, Response
from typing import Optional

WHOP_CLIENT_ID = os.getenv("WHOP_CLIENT_ID")
WHOP_CLIENT_SECRET = os.getenv("WHOP_CLIENT_SECRET")
WHOP_REDIRECT_URI = os.getenv("WHOP_REDIRECT_URI") # e.g. https://your-site.com/api/auth/callback

async def exchange_code_for_token(code: str):
    """Exchanges Whop OAuth code for access token."""
    url = "https://data.whop.com/api/v5/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": WHOP_CLIENT_ID,
        "client_secret": WHOP_CLIENT_SECRET,
        "redirect_uri": WHOP_REDIRECT_URI
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=payload)
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Failed to exchange Whop code")
        return response.json()

async def get_whop_user(access_token: str):
    """Fetches user info and memberships from Whop."""
    url = "https://data.whop.com/api/v5/me"
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Failed to fetch Whop user")
        return response.json()

async def validate_user_subscription(memberships: list):
    """Validates if the user has the required active plan."""
    target_plan_id = os.getenv("WHOP_PLAN_ID")
    for membership in memberships:
        if membership.get("plan_id") == target_plan_id and membership.get("status") == "active":
            return True
    return False
