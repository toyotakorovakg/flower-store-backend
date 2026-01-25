"""
    Message service.

    Provides functions for retrieving and creating chat messages.
    In a real application, this service would enforce row‑level security
    to ensure that actors only see messages they are permitted to view.
"""
from __future__ import annotations

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.message import Message
from app.schemas.message import MessageCreate


async def get_messages(db: AsyncSession) -> List[Message]:
    """Return all messages."""
    result = await db.execute(select(Message))
    return result.scalars().all()


async def create_message(db: AsyncSession, message_in: MessageCreate) -> Message:
    """Create a new chat message and persist it to the database."""
    new_message = Message(
        session_id=message_in.session_id,
        client_id=message_in.client_id,
        support_id=message_in.support_id,
        content=message_in.content,
        chat_type=message_in.chat_type,
        is_from_client=message_in.is_from_client,
        metadata_json=message_in.metadata,
    )
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)
    return new_message
