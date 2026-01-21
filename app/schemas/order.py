"""
Pydantic schemas for order data.

Defines the response model for order information.  The ``model_config``
attribute enables validation from SQLAlchemy ORM instances when using
``model_validate``.  See the Pydantic v2 migration guide for details.
"""

from pydantic import BaseModel, ConfigDict


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
