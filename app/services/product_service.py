"""
Product service.

Provides functions to retrieve products from the database. In a full
implementation, additional functions would support creating and updating
products with appropriate validation and permission checks.
"""

from __future__ import annotations

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.product import Product


async def get_products(db: AsyncSession) -> List[Product]:
    """Return all active products."""
    result = await db.execute(select(Product).where(Product.is_active == True))  # noqa: E712
    return result.scalars().all()
