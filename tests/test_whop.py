import unittest
from unittest.mock import patch, MagicMock
from core.whop_client import WhopClient

class TestWhopClient(unittest.TestCase):
    def setUp(self):
        # نستخدم مفتاح وهمي للاختبارات
        self.client = WhopClient(api_key="test_key")

    @patch('requests.get')
    def test_get_user_memberships_success(self, mock_get):
        # إعداد الرد الوهمي
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"product_id": "prod_1", "status": "active"}]}
        mock_get.return_value = mock_response

        result = self.client.get_user_memberships("user_123")
        self.assertIn("data", result)
        self.assertEqual(result["data"][0]["product_id"], "prod_1")

    @patch('requests.get')
    def test_validate_access_active(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"product_id": "prod_1", "status": "active"}]}
        mock_get.return_value = mock_response

        has_access = self.client.validate_access("user_123", "prod_1")
        self.assertTrue(has_access)

    @patch('requests.get')
    def test_validate_access_inactive(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"product_id": "prod_1", "status": "expired"}]}
        mock_get.return_value = mock_response

        has_access = self.client.validate_access("user_123", "prod_1")
        self.assertFalse(has_access)

if __name__ == '__main__':
    unittest.main()
