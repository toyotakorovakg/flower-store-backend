"""
Time utilities.

Centralised helpers for working with timezone-aware datetime objects. Use
these functions instead of calling datetime.utcnow directly to ensure
consistent time handling across the application.
"""

from __future__ import annotations

import datetime


def utcnow() -> datetime.datetime:
    """Return the current UTC time with timezone information."""
    return datetime.datetime.now(tz=datetime.timezone.utc)
