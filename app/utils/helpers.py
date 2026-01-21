"""
Miscellaneous helper functions.
"""

from __future__ import annotations

import uuid


def generate_uuid() -> str:
    """Generate a random UUID string.

    Although the database generates UUIDs itself, sometimes a client may
    need to create a UUID for idempotent requests. This helper uses
    Python's uuid4 for randomness.
    """
    return str(uuid.uuid4())
