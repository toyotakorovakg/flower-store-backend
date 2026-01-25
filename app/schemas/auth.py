"""
    Pydantic models for authentication requests and responses.
"""
from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RegisterRequest(BaseModel):
    """Request body for user registration."""
    email: EmailStr
    password: str
    full_name: str | None = None
    phone: str | None = None
    address: str | None = None

class RegisterResponse(BaseModel):
    """Response body for successful registration."""
    user_id: str
    access_token: str
    token_type: str = "bearer"
