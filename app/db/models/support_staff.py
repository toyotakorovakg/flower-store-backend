"""
SupportStaff model definition.
"""

import uuid
from sqlalchemy import Column, String, Boolean, Integer, DateTime, SmallInteger, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.base import Base


class SupportStaff(Base):
    __tablename__ = "support_staff"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email_hash = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    password_changed_at = Column(DateTime(timezone=True), server_default=func.now())
    full_name = Column(String, nullable=False)
    role = Column(String, nullable=False, server_default="support")
    permissions = Column(JSON, nullable=False, server_default="[]")
    is_active = Column(Boolean, nullable=False, server_default="true")
    requires_2fa = Column(Boolean, nullable=False, server_default="true")
    failed_login_count = Column(SmallInteger, nullable=False, server_default="0")
    locked_until = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    version = Column(Integer, nullable=False, server_default="1")
