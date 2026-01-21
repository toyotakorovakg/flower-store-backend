"""
User management endpoints.

Provides CRUD operations for users (customers and support staff). All
handlers should enforce appropriate row‑level security via the database.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.user import User as UserSchema
from app.services.user_service import get_users


router = APIRouter()


@router.get("/", summary="List users", response_model=list[UserSchema])
async def list_users(db: AsyncSession = Depends(get_session)) -> list[UserSchema]:
    """Return a list of users visible to the current actor."""
    users = await get_users(db)
    # Use model_validate instead of from_orm for Pydantic v2
    return [UserSchema.model_validate(u) for u in users]
