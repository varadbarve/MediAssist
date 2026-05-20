"""
Layer 5 — Phone Number Encryption at Rest
Uses Fernet symmetric encryption (AES-128-CBC + HMAC-SHA256) from the
`cryptography` library (free, BSD license).
"""

from cryptography.fernet import Fernet, InvalidToken
from app.core.config import ENCRYPTION_KEY


_cached_fernet = None


def _get_fernet() -> Fernet:
    """Get a Fernet instance. If no key is configured, generate one and warn."""
    global _cached_fernet
    if _cached_fernet is not None:
        return _cached_fernet

    key = ENCRYPTION_KEY
    if not key:
        # Auto-generate a key and print it so the developer can save it
        key = Fernet.generate_key().decode()
        print("\n" + "=" * 60)
        print("WARNING: No ENCRYPTION_KEY set in .env!")
        print("A temporary key has been generated for this session.")
        print("Add this to your .env file to persist encrypted data:")
        print(f"  ENCRYPTION_KEY={key}")
        print("=" * 60 + "\n")
        _cached_fernet = Fernet(key.encode())
        return _cached_fernet

    _cached_fernet = Fernet(key.encode())
    return _cached_fernet


def encrypt_value(plaintext: str) -> str:
    """Encrypt a string value. Returns base64-encoded ciphertext."""
    if not plaintext:
        return ""
    f = _get_fernet()
    return f.encrypt(plaintext.encode()).decode()


def decrypt_value(ciphertext: str) -> str:
    """Decrypt a base64-encoded ciphertext. Returns plaintext string."""
    if not ciphertext:
        return ""
    f = _get_fernet()
    try:
        return f.decrypt(ciphertext.encode()).decode()
    except InvalidToken:
        # If decryption fails, the data might be plain text (pre-encryption)
        # or the key has changed. Return a masked value for safety.
        return "***DECRYPTION_FAILED***"
