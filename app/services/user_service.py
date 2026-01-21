"""
User service.

Provides database operations for the unified users view. Note that the
``users_view`` is a PostgreSQL view defined in the SQL schema, so this
service should treat it as read-only.
"""

from __future__ import annotations

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User


async def get_users(db: AsyncSession) -> List[User]:
    """Return all users visible to the current actor.

    In this simplified implementation, no RLS filtering is applied. The
    caller should ensure the session variables are set appropriately
    before invoking this function.
    """
    result = await db.execute(select(User))
    return result.scalars().all()
