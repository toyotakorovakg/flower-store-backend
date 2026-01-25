"""
    Authentication endpoints.

    Handles user login, registration and logout. Registration creates a
    new customer, login issues a JWT, and logout simply instructs the client
    to discard its token (stateless JWTs cannot be revoked server‑side without
    additional infrastructure).
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    RegisterRequest,
    RegisterResponse,
)
from app.services.auth_service import (
    login as login_service,
    register_user as register_service,
)
from app.db.session import get_session

router = APIRouter()

@router.post("/login", response_model=TokenResponse, summary="Login user")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_session)) -> TokenResponse:
    """Authenticate the user and return an access token upon success."""
    result = await login_service(db, request.email, request.password)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return TokenResponse(**result)

@router.post("/register", response_model=RegisterResponse, summary="Register new customer")
async def register(
    request: RegisterRequest, db: AsyncSession = Depends(get_session)
) -> RegisterResponse:
    """Create a new customer account and return a token."""
    result = await register_service(
        db,
        email=request.email,
        password=request.password,
        full_name=request.full_name,
        phone=request.phone,
        address=request.address,
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists",
        )
    return RegisterResponse(**result)

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, summary="Logout current user")
async def logout() -> Response:
    """Logout endpoint. Clients should delete their JWT on logout."""
    return Response(status_code=status.HTTP_204_NO_CONTENT)
