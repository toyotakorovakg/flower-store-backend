"""
    Pydantic schemas for order data.

    Defines both the response model (OrderOut) and the request model
    (OrderCreate).  The request model is used when creating orders via POST.
"""
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class OrderCreate(BaseModel):
    """Schema for creating a new order."""

    client_id: UUID
    subtotal_cents: int
    discount_cents: int = 0
    shipping_cents: int = 0
    tax_cents: int = 0
    total_cents: int
    currency: str = "USD"
    status: str = "pending"
    notes: Optional[str] = None
    internal_notes: Optional[str] = None


class OrderOut(BaseModel):
    id: str
    order_number: int | None
    client_id: str
    subtotal_cents: int
    discount_cents: int
    shipping_cents: int
    tax_cents: int
    total_cents: int
    currency: str
    status: str
    notes: str | None
    internal_notes: str | None

    model_config = ConfigDict(from_attributes=True)
