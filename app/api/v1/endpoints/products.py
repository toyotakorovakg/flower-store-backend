"""
    Product endpoints.

    Handles creation, update and listing of products.  Access controls depend on
    actor role.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.product import ProductOut, ProductCreate
from app.services.product_service import get_products, create_product

router = APIRouter()


@router.get("/", summary="List products", response_model=list[ProductOut])
async def list_products(db: AsyncSession = Depends(get_session)) -> list[ProductOut]:
    """Return a list of products."""
    products = await get_products(db)
    return [ProductOut.model_validate(p) for p in products]


@router.post(
    "/",
    summary="Create product",
    response_model=ProductOut,
    status_code=status.HTTP_201_CREATED,
)
async def add_product(
    product_in: ProductCreate,
    db: AsyncSession = Depends(get_session),
) -> ProductOut:
    """Create a new product."""
    product = await create_product(db, product_in)
    return ProductOut.model_validate(product)
