"""
Pydantic schemas for order data.
"""

from pydantic import BaseModel


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

    class Config:
        orm_mode = True
