"""
    Cryptographic helper functions.

    Provides utilities for hashing email addresses using a secret pepper and
    verifying or creating password hashes. Password hashing delegates to the
    security module's CryptContext (bcrypt), while email hashing uses SHA-256.
"""
from __future__ import annotations

import hashlib

from app.core.settings import settings


def hash_email(email: str) -> bytes:
    """Return a SHA-256 digest of the email address concatenated with a pepper.

    Email addresses are normalised to lower case before hashing. The pepper
    comes from the application settings and must be kept secret. The returned
    digest is a byte string suitable for storage in a BYTEA column.
    """
    normalized = email.strip().lower()
    pepper = settings.email_pepper
    digest = hashlib.sha256((normalized + pepper).encode("utf-8")).digest()
    return digest
