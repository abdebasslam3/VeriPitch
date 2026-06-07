import unittest
from unittest.mock import patch, MagicMock
from core.whop_client import WhopClient

class TestWhopClient(unittest.TestCase):
    def setUp(self):
        self.client = WhopClient(api_key="test_key")

    @patch('whop_sdk.Whop')
    def test_get_user_memberships_sdk(self, mock_whop):
        # Mock the SDK response
        mock_membership = MagicMock()
        mock_membership.product_id = "prod_1"
        mock_membership.status = "active"

        mock_list_response = MagicMock()
        mock_list_response.data = [mock_membership]

        # Setup mock client
        self.client.client.memberships.list = MagicMock(return_value=mock_list_response)

        result = self.client.get_user_memberships("user_123")
        self.assertTrue(hasattr(result, 'data'))
        self.assertEqual(result.data[0].product_id, "prod_1")

    @patch('whop_sdk.Whop')
    def test_validate_access_active_sdk(self, mock_whop):
        mock_membership = MagicMock()
        mock_membership.product_id = "prod_1"
        mock_membership.status = "active"

        mock_list_response = MagicMock()
        mock_list_response.data = [mock_membership]

        self.client.client.memberships.list = MagicMock(return_value=mock_list_response)

        has_access = self.client.validate_access("user_123", "prod_1")
        self.assertTrue(has_access)

if __name__ == '__main__':
    unittest.main()
