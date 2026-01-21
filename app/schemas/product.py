"""
Pydantic schemas for product data.
"""

from pydantic import BaseModel


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

    class Config:
        orm_mode = True
