"""
Authentication service.

This module implements user authentication by verifying email and password
against the database. It leverages the crypto utilities to hash email
addresses and the security module to verify password hashes.
"""

from __future__ import annotations

import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password, create_access_token
from app.db.models.customer import Customer
from app.db.models.support_staff import SupportStaff
from app.utils.crypto import hash_email
from app.utils.time import utcnow

# Constants controlling lockout behaviour
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15


async def authenticate_user(
    db: AsyncSession, email: str, password: str
) -> tuple[Optional[str], Optional[str]]:
    """Authenticate a user by email and password.

    Returns a tuple of (user_id, role) on success or (None, None) on failure.
    Searches both the customers and support_staff tables. For customers,
    the user role is ``customer``; for support staff, it is the value of
    the ``role`` column (e.g. ``support`` or ``admin``).
    """
    email_hash = hash_email(email)

    # Try customer
    result = await db.execute(
        select(Customer).where(Customer.email_hash == email_hash)
    )
    customer = result.scalar_one_or_none()
    if customer and verify_password(password, customer.password_hash):
        return str(customer.id), "customer"

    # Try support staff
    result = await db.execute(
        select(SupportStaff).where(SupportStaff.email_hash == email_hash)
    )
    staff = result.scalar_one_or_none()
    if staff and verify_password(password, staff.password_hash):
        return str(staff.id), staff.role

    return None, None


async def login(
    db: AsyncSession, email: str, password: str
) -> Optional[dict]:
    """Attempt to log in the user and return a token response.

    This implementation adds basic brute‑force protection. It tracks the number
    of failed login attempts on each account and temporarily locks the account
    after a configurable number of consecutive failures. When a lock is
    active, all login attempts will be rejected until the lock period
    expires. On successful authentication the counters are reset.
    """
    email_hash = hash_email(email)
    now = utcnow()

    async def _process_failed_login(user) -> None:
        """Increment failed count and lock account if threshold exceeded."""
        current = user.failed_login_count or 0
        current += 1
        if current >= MAX_FAILED_ATTEMPTS:
            user.locked_until = utcnow() + datetime.timedelta(minutes=LOCKOUT_DURATION_MINUTES)
            user.failed_login_count = 0
        else:
            user.failed_login_count = current
        await db.commit()
        await db.refresh(user)

    async def _reset_login_attempts(user) -> None:
        """Clear counters and unlock the account on successful login."""
        user.failed_login_count = 0
        user.locked_until = None
        await db.commit()
        await db.refresh(user)

    # Try customer first
    result = await db.execute(select(Customer).where(Customer.email_hash == email_hash))
    customer = result.scalar_one_or_none()
    if customer:
        # Check if account is currently locked
        if customer.locked_until and customer.locked_until > now:
            return None
        if verify_password(password, customer.password_hash):
            await _reset_login_attempts(customer)
            token = create_access_token(
                subject=str(customer.id),
                additional_claims={"role": "customer"},
            )
            return {"access_token": token, "token_type": "bearer"}
        # Incorrect password; update failure count
        await _process_failed_login(customer)
        return None

    # Then try support staff
    result = await db.execute(select(SupportStaff).where(SupportStaff.email_hash == email_hash))
    staff = result.scalar_one_or_none()
    if staff:
        if staff.locked_until and staff.locked_until > now:
            return None
        if verify_password(password, staff.password_hash):
            await _reset_login_attempts(staff)
            token = create_access_token(
                subject=str(staff.id),
                additional_claims={"role": staff.role},
            )
            return {"access_token": token, "token_type": "bearer"}
        await _process_failed_login(staff)
        return None

    # No user found
    return None
