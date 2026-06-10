import pytest
from unittest.mock import MagicMock, patch

# Mock environment variables before importing app
with patch.dict('os.environ', {
    'SUPABASE_URL': 'https://test.supabase.co',
    'SUPABASE_SERVICE_ROLE_KEY': 'test_key',
    'WHOP_CLIENT_ID': 'test_id',
    'WHOP_CLIENT_SECRET': 'test_secret',
    'WHOP_PLAN_ID': 'test_plan',
    'WHOP_API_KEY': 'test_api_key'
}):
    from main import app
    from core.matcher import SkillMatcher
    from core.utils.encryption import decrypt_api_key, generate_dynamic_salt

def test_encryption_integrity():
    salt = generate_dynamic_salt()
    original_key = "sk-test-key-12345"

    from cryptography.fernet import Fernet
    import base64
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    password = salt.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'veripitch_static_salt',
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    encrypted = f.encrypt(original_key.encode()).decode()

    decrypted = decrypt_api_key(encrypted, salt)
    assert decrypted == original_key

def test_matcher_precision():
    user_skills = ["React", "Node.js", "C++", "Tailwind CSS"]
    matcher = SkillMatcher(user_skills)

    job_desc = "We need a C++ developer who knows React and Node.js. Experience with Tailwind CSS is a plus."
    report = matcher.analyze_job(job_desc)

    assert "c++" in report["matched"]
    assert "node.js" in report["matched"]
    assert "react" in report["matched"]
    assert "tailwind css" in report["matched"]
    # Ensure it doesn't match 'tailwind' and 'css' separately if 'tailwind css' is matched
    assert "tailwind" not in report["matched"]
    assert len(report["missing"]) == 0

def test_backend_routing_integrity():
    routes = [route.path for route in app.routes]

    expected_routes = [
        "/",
        "/api/v1/health",
        "/api/v1/generate-proposal",
        "/api/v1/check-api-key",
        "/api/v1/upload-resume",
        "/api/v1/ingest-text-profile",
        "/api/v1/check-cooldown",
        "/api/v1/start-smart-quiz",
        "/api/v1/verify-quiz-answer",
        "/api/v1/webhooks/whop",
        "/api/v1/auth/callback"
    ]

    for route in expected_routes:
        assert route in routes
