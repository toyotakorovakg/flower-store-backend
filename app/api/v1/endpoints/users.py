"""
User management endpoints.

Provides CRUD operations for users (customers and support staff). All
handlers should enforce appropriate row‑level security via the database.
"""
from __future__ import annotations

from typing import List

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
    return [UserSchema.from_orm(u) for u in users]
