"""
Message service.

Provides functions for retrieving chat messages. In a real application, this
service would enforce row-level security to ensure that actors only see
messages they are permitted to view. Here, we simply return all messages.
"""

from __future__ import annotations

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.message import Message


async def get_messages(db: AsyncSession) -> List[Message]:
    """Return all messages."""
    result = await db.execute(select(Message))
    return result.scalars().all()
