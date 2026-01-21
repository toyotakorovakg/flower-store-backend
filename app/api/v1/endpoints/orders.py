"""
Order endpoints.

CRUD operations on orders and order items. Properly apply RLS by ensuring
the database context is set for each request.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.order import OrderOut
from app.services.order_service import get_orders

router = APIRouter()


@router.get("/", summary="List orders", response_model=list[OrderOut])
async def list_orders(db: AsyncSession = Depends(get_session)) -> list[OrderOut]:
    """Return a list of orders visible to the current user."""
    orders = await get_orders(db)
    return [OrderOut.from_orm(o) for o in orders]
