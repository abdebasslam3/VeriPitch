import requests
import os
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class WhopClient:
    """
    WhopClient
    Handles integration with Whop API for authentication and membership validation.
    """
    BASE_URL = "https://api.whop.com/v1"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initializes the client with the Whop API Key.
        """
        self.api_key = api_key or os.getenv("WHOP_API_KEY")
        if not self.api_key:
            logging.error("Whop API Key is missing.")
            raise ValueError("Whop API Key is required.")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def get_user_memberships(self, user_id: str) -> Dict[str, Any]:
        """
        Fetches memberships for a specific user from Whop.

        استرجاع عضويات مستخدم معين من Whop.
        """
        try:
            url = f"{self.BASE_URL}/memberships"
            params = {"user_id": user_id}
            response = requests.get(url, headers=self.headers, params=params)

            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"Failed to fetch memberships: {response.status_code} - {response.text}")
                return {"error": "API Request failed", "status_code": response.status_code}
        except Exception as e:
            logging.exception("Exception occurred while calling Whop API.")
            return {"error": str(e)}

    def validate_access(self, user_id: str, product_id: str) -> bool:
        """
        Checks if a user has an active membership for a specific product.

        التحقق مما إذا كان للمستخدم عضوية نشطة لمنتج معين.
        """
        memberships = self.get_user_memberships(user_id)
        if "data" in memberships:
            for membership in memberships["data"]:
                if membership.get("product_id") == product_id and membership.get("status") == "active":
                    return True
        return False

if __name__ == "__main__":
    # Quick manual test
    try:
        # Load .env manually for standalone run if needed
        from dotenv import load_dotenv
        load_dotenv()

        client = WhopClient()
        print("Whop Client Initialized Successfully.")
    except Exception as e:
        print(f"Initialization Failed: {e}")
