"""
Authentication service.

This module implements user authentication by verifying email and password
against the database. It leverages the crypto utilities to hash email
addresses and the security module to verify password hashes.
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password, create_access_token
from app.db.models.customer import Customer
from app.db.models.support_staff import SupportStaff
from app.utils.crypto import hash_email


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

    If authentication succeeds, create a JWT access token with the subject
    set to the user ID and include the user's role as a custom claim.
    """
    user_id, role = await authenticate_user(db, email, password)
    if not user_id:
        return None
    token = create_access_token(
        subject=user_id,
        additional_claims={"role": role},
    )
    return {"access_token": token, "token_type": "bearer"}
