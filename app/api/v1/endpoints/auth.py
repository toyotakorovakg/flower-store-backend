"""
Authentication endpoints.

Handles user login and token issuance. In a real application, this module
would integrate with the database to verify users and enforce two‑factor
authentication.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import login as login_service
from app.db.session import get_session

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_session)) -> TokenResponse:
    """Authenticate the user and return an access token upon success."""
    result = await login_service(db, request.email, request.password)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return TokenResponse(**result)
