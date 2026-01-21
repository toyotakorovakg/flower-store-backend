"""
SQLAlchemy model for products.

This model maps to the ``products`` table in the database. It stores
information about items that can be purchased in the flower store.
"""

from __future__ import annotations

import uuid
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    DateTime,
    BigInteger,
    CheckConstraint,
    CHAR,
    func,
)
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


class Product(Base):
    """Represents a purchasable product in the store."""

    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id = Column(UUID(as_uuid=True), nullable=True)  # foreign key omitted
    sku = Column(String, nullable=False, unique=True)
    slug = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price_cents = Column(BigInteger, nullable=False)
    compare_at_price_cents = Column(BigInteger, nullable=True)
    currency = Column(CHAR(3), nullable=False, server_default="USD")
    stock = Column(Integer, nullable=False, server_default="0")
    reserved_stock = Column(Integer, nullable=False, server_default="0")
    low_stock_threshold = Column(Integer, nullable=False, server_default="5")
    weight_grams = Column(Integer, nullable=True)
    is_active = Column(Boolean, nullable=False, server_default="true")
    is_featured = Column(Boolean, nullable=False, server_default="false")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    version = Column(Integer, nullable=False, server_default="1")

    __table_args__ = (
        CheckConstraint("stock >= 0", name="ck_product_stock_non_negative"),
        CheckConstraint(
            "reserved_stock <= stock", name="ck_product_reserved_le_stock"
        ),
    )
