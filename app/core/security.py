"""
Security utilities for authentication and encryption.

This module centralises logic for password hashing, token generation and
verification. In production, ensure that chosen algorithms and parameters
adhere to current best practices.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, Optional

from jose import JWTError, jwt  # python-jose
from passlib.context import CryptContext
from fastapi import HTTPException, status

from app.core.settings import settings

# Password hashing context. The bcrypt scheme defaults to a secure cost factor.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Return True if the provided plain password matches the hashed value."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a new password using bcrypt."""
    return pwd_context.hash(password)


def create_access_token(
    subject: str,
    expires_delta: Optional[datetime.timedelta] = None,
    additional_claims: Optional[Dict[str, Any]] = None,
) -> str:
    """Generate a JWT access token for the given subject."""
    to_encode: Dict[str, Any] = {"sub": subject}
    if additional_claims:
        to_encode.update(additional_claims)
    expire = datetime.datetime.utcnow() + (
        expires_delta or datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def verify_jwt(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT.

    Raises HTTPException on failure. Returns the decoded payload if valid.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception
