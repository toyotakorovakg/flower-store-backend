"""
    Order endpoints.

    CRUD operations on orders and order items.  Properly apply RLS by ensuring
    the database context is set for each request.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.order import OrderOut, OrderCreate
from app.services.order_service import get_orders, create_order

router = APIRouter()


@router.get("/", summary="List orders", response_model=list[OrderOut])
async def list_orders(db: AsyncSession = Depends(get_session)) -> list[OrderOut]:
    """Return a list of orders visible to the current user."""
    orders = await get_orders(db)
    return [OrderOut.model_validate(o) for o in orders]


@router.post(
    "/",
    summary="Create order",
    response_model=OrderOut,
    status_code=status.HTTP_201_CREATED,
)
async def add_order(
    order_in: OrderCreate,
    db: AsyncSession = Depends(get_session),
) -> OrderOut:
    """Create a new order."""
    order = await create_order(db, order_in)
    return OrderOut.model_validate(order)
