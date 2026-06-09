from core.utils.encryption import decrypt_api_key, generate_dynamic_salt
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def test_encryption_cycle():
    dynamic_salt = "test_salt_123"
    raw_key = "sk-test-12345"

    # Simulate frontend encryption (simplified for test)
    password = dynamic_salt.encode()
    salt = b'veripitch_static_salt'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    encrypted_key = f.encrypt(raw_key.encode()).decode()

    # Backend decryption
    decrypted = decrypt_api_key(encrypted_key, dynamic_salt)
    assert decrypted == raw_key
