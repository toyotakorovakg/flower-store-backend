"""
Encryption and decryption service.

Provides functions for encrypting and decrypting text using a symmetric
algorithm. The encryption key is loaded from configuration and must be a
32-byte base64-encoded key compatible with Fernet.

If the cryptography package is not installed, the functions will raise
ImportError at runtime. Install ``cryptography`` to use this service.
"""

from __future__ import annotations

from typing import Optional

from app.core.settings import settings

try:
    from cryptography.fernet import Fernet, InvalidToken
except ImportError:  # pragma: no cover - cryptography is optional
    Fernet = None  # type: ignore
    InvalidToken = Exception  # type: ignore


def _get_fernet() -> Fernet:
    if Fernet is None:
        raise ImportError("cryptography is required for encryption/decryption")
    key = settings.encryption_key.encode("utf-8")
    return Fernet(key)


def encrypt_text(plain: str) -> str:
    """Encrypt plain text and return a base64-encoded string."""
    f = _get_fernet()
    return f.encrypt(plain.encode("utf-8")).decode("utf-8")


def decrypt_text(token: str) -> Optional[str]:
    """Decrypt a previously encrypted string.

    Returns None if the token cannot be decrypted.
    """
    f = _get_fernet()
    try:
        return f.decrypt(token.encode("utf-8")).decode("utf-8")
    except InvalidToken:
        return None
