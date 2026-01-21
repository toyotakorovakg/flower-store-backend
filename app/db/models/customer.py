"""
Customer model definition.
"""

import uuid
from sqlalchemy import Column, String, Boolean, Integer, DateTime, SmallInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.base import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email_hash = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    password_algo = Column(String, nullable=False, server_default="bcrypt")
    password_changed_at = Column(DateTime(timezone=True), server_default=func.now())
    full_name_enc = Column(String, nullable=True)
    phone_enc = Column(String, nullable=True)
    address_enc = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, server_default="true")
    is_verified = Column(Boolean, nullable=False, server_default="false")
    verified_at = Column(DateTime(timezone=True), nullable=True)
    failed_login_count = Column(SmallInteger, nullable=False, server_default="0")
    locked_until = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    version = Column(Integer, nullable=False, server_default="1")
