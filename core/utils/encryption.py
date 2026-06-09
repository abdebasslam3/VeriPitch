from cryptography.fernet import Fernet
import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def decrypt_api_key(encrypted_key: str, dynamic_salt: str) -> str:
    """
    Decrypts the API key using the dynamic salt provided by the client/session.
    This is part of the Zero-Knowledge architecture.
    """
    password = dynamic_salt.encode()
    salt = b'veripitch_static_salt' # In a real scenario, this could also be dynamic but needs to be consistent

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)

    try:
        decrypted_key = f.decrypt(encrypted_key.encode()).decode()
        return decrypted_key
    except Exception:
        raise ValueError("Failed to decrypt API key. Invalid salt or corrupted data.")

def generate_dynamic_salt():
    """Generates a random dynamic salt for the session."""
    return base64.b64encode(os.urandom(16)).decode()
