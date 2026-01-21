"""
Common dependency functions for API endpoints.

These dependencies handle authentication, authorization and provide
database sessions. They should perform proper checks based on user roles and
raise exceptions when access is denied.
"""
from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_jwt
from app.db.session import get_session
from app.db.models.customer import Customer
from app.db.models.support_staff import SupportStaff

import uuid

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_db_session() -> AsyncSession:
    """Provide a database session to request handlers."""
    async for session in get_session():  # type: ignore[assignment]
        return session


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db_session)
) -> dict:
    """Retrieve the current user based on a JWT bearer token.

    Decodes the JWT using ``verify_jwt`` and then loads the user from either
    the customers or support_staff tables. Raises HTTPException if the
    token is invalid or if the user no longer exists.
    """
    payload = verify_jwt(token)
    user_id: str = payload.get("sub")  # subject contains UUID string
    role: str = payload.get("role")
    if not user_id or not role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    # Attempt to load the user from the appropriate table
    if role == "customer":
        result = await db.get(Customer, uuid.UUID(user_id))
        user_obj = result
    else:
        result = await db.get(SupportStaff, uuid.UUID(user_id))
        user_obj = result
    if user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return {"id": user_id, "role": role}

