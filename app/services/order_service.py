"""
    Order service.

    Provides operations for retrieving and creating orders.  In a real
    implementation, row‑level security should restrict the orders returned or
    created based on the current user context.
"""
from __future__ import annotations

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.order import Order
from app.schemas.order import OrderCreate


async def get_orders(db: AsyncSession) -> List[Order]:
    """Return all orders.

    The caller should ensure that RLS context variables are set so that
    the underlying query is filtered appropriately by the database.
    """
    result = await db.execute(select(Order))
    return result.scalars().all()


async def create_order(db: AsyncSession, order_in: OrderCreate) -> Order:
    """Create a new order and persist it to the database."""
    new_order = Order(
        client_id=order_in.client_id,
        subtotal_cents=order_in.subtotal_cents,
        discount_cents=order_in.discount_cents,
        shipping_cents=order_in.shipping_cents,
        tax_cents=order_in.tax_cents,
        total_cents=order_in.total_cents,
        currency=order_in.currency,
        status=order_in.status,
        notes=order_in.notes,
        internal_notes=order_in.internal_notes,
    )
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order
