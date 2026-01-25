"""
    Product service.

    Provides functions to retrieve, create, and update products from the database.
    Functions return ORM objects that can be converted to Pydantic models using
    ``model_validate``.
"""
from __future__ import annotations

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.product import Product
from app.schemas.product import ProductCreate


async def get_products(db: AsyncSession) -> List[Product]:
    """Return all active products."""
    result = await db.execute(select(Product).where(Product.is_active == True))  # noqa: E712
    return result.scalars().all()


async def create_product(db: AsyncSession, product_in: ProductCreate) -> Product:
    """Create a new product and persist it to the database."""
    new_product = Product(
        sku=product_in.sku,
        slug=product_in.slug,
        name=product_in.name,
        description=product_in.description,
        price_cents=product_in.price_cents,
        compare_at_price_cents=product_in.compare_at_price_cents,
        currency=product_in.currency,
        stock=product_in.stock,
        reserved_stock=product_in.reserved_stock,
        low_stock_threshold=product_in.low_stock_threshold,
        weight_grams=product_in.weight_grams,
        is_active=product_in.is_active,
        is_featured=product_in.is_featured,
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product
