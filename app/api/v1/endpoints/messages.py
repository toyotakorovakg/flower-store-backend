"""
    Chat and messaging endpoints.

    Messages between customers and support staff (or AI bot).  Apply RLS
    policies and encryption/decryption as needed.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.message import MessageOut, MessageCreate
from app.services.message_service import get_messages, create_message

router = APIRouter()


@router.get("/", summary="List messages", response_model=list[MessageOut])
async def list_messages(db: AsyncSession = Depends(get_session)) -> list[MessageOut]:
    """List messages available to the current actor."""
    messages = await get_messages(db)
    return [MessageOut.model_validate(m) for m in messages]


@router.post(
    "/",
    summary="Create message",
    response_model=MessageOut,
    status_code=status.HTTP_201_CREATED,
)
async def add_message(
    message_in: MessageCreate,
    db: AsyncSession = Depends(get_session),
) -> MessageOut:
    """Create a new chat message."""
    message = await create_message(db, message_in)
    return MessageOut.model_validate(message)
