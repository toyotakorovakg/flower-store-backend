"""
Chat and messaging endpoints.

Messages between customers and support staff (or AI bot). Apply RLS
policies and encryption/decryption as needed.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.message import MessageOut
from app.services.message_service import get_messages


router = APIRouter()


@router.get("/", summary="List messages", response_model=list[MessageOut])
async def list_messages(db: AsyncSession = Depends(get_session)) -> list[MessageOut]:
    """List messages available to the current actor."""
    messages = await get_messages(db)
    return [MessageOut.model_validate(m) for m in messages]
