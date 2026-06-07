import os
import logging
from typing import Any, Optional
from whop_sdk import Whop

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class WhopClient:
    """
    WhopClient
    Handles integration with Whop API using the official SDK.
    """
    def __init__(self, api_key: Optional[str] = None):
        """
        Initializes the client with the Whop API Key using official SDK.
        """
        self.api_key = api_key or os.getenv("WHOP_API_KEY")
        if not self.api_key:
            logging.error("Whop API Key is missing.")
            raise ValueError("Whop API Key is required.")

        # Initialize official Whop SDK client
        self.client = Whop(api_key=self.api_key)

    def get_user_memberships(self, user_id: str) -> Any:
        """
        Fetches memberships for a specific user using Whop SDK.
        """
        try:
            # Using SDK to fetch memberships
            memberships = self.client.memberships.list(user_id=user_id)
            return memberships
        except Exception as e:
            logging.exception(f"Error fetching memberships via SDK: {e}")
            return {"error": str(e)}

    def validate_access(self, user_id: str, product_id: str) -> bool:
        """
        Checks if a user has an active membership for a specific product.
        """
        try:
            memberships = self.get_user_memberships(user_id)
            # Official SDK returns objects, let's check for data
            if hasattr(memberships, 'data'):
                for membership in memberships.data:
                    if membership.product_id == product_id and membership.status == "active":
                        return True
            return False
        except Exception:
            return False

if __name__ == "__main__":
    # Test initialization
    try:
        from dotenv import load_dotenv
        load_dotenv()
        client = WhopClient()
        print("Whop SDK Client Initialized.")
    except Exception as e:
        print(f"Error: {e}")
