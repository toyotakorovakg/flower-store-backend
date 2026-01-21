"""
Cryptographic helper functions.

This module provides utilities for hashing email addresses using a secret
pepper and verifying or creating password hashes. Password hashing
delegates to the security module's CryptContext (bcrypt), while email
hashing uses SHA-256 with a pepper to avoid simple rainbow-table attacks.
"""

from __future__ import annotations

import hashlib
from typing import Optional

from app.core.settings import settings


def hash_email(email: str) -> str:
    """Return a SHA-256 hash of the email address concatenated with a pepper.

    Email addresses are normalised to lower case before hashing. The pepper
    comes from the application settings and must be kept secret.
    The returned hash is a hexadecimal string.
    """
    normalized = email.strip().lower()
    pepper = settings.email_pepper
    digest = hashlib.sha256((normalized + pepper).encode("utf-8")).hexdigest()
    return digest
