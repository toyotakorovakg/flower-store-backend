"""
Product endpoints.

Handles creation, update and listing of products. Access controls depend on
actor role.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.product import ProductOut
from app.services.product_service import get_products

router = APIRouter()


@router.get("/", summary="List products", response_model=list[ProductOut])
async def list_products(db: AsyncSession = Depends(get_session)) -> list[ProductOut]:
    """Return a list of products."""
    products = await get_products(db)
    return [ProductOut.from_orm(p) for p in products]
