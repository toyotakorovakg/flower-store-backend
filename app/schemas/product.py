"""
    Pydantic schemas for product data.

    Defines both the response model (ProductOut) and the request model
    (ProductCreate).  The request model is used when creating new products via
    POST requests.  Instances of these schemas can be constructed from
    SQLAlchemy ORM objects via the ``model_validate`` method.
"""
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    """Schema for creating a new product."""

    sku: str
    slug: str
    name: str
    description: Optional[str] = None
    price_cents: int
    compare_at_price_cents: Optional[int] = None
    currency: str = "USD"
    stock: int = 0
    reserved_stock: int = 0
    low_stock_threshold: int = 5
    weight_grams: Optional[int] = None
    is_active: bool = True
    is_featured: bool = False


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
