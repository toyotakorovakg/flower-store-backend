"""
Pydantic schemas for product data.

Represents a product returned from the API.  When combined with
``model_config = ConfigDict(from_attributes=True)``, instances can be created
directly from SQLAlchemy ORM objects using the ``model_validate`` method.
"""

from pydantic import BaseModel, ConfigDict


class ProductOut(BaseModel):
    id: str
    sku: str
    slug: str
    name: str
    description: str | None
    price_cents: int
    compare_at_price_cents: int | None
    currency: str
    stock: int
    reserved_stock: int
    low_stock_threshold: int
    weight_grams: int | None
    is_active: bool
    is_featured: bool

    model_config = ConfigDict(from_attributes=True)
