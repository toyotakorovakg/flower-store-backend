"""
Order service.

Provides operations for retrieving orders. In a real implementation, this
service would apply row-level security by filtering on the current user
context. For demonstration purposes, we return all orders.
"""

from __future__ import annotations

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.order import Order


async def get_orders(db: AsyncSession) -> List[Order]:
    """Return all orders.

    The caller should ensure that RLS context variables are set so that
    the underlying query is filtered appropriately by the database.
    """
    result = await db.execute(select(Order))
    return result.scalars().all()
