"""
AuditLog model definition.

This model records changes to other tables. It maps to the audit_logs table.
"""

import uuid
from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func

from app.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    table_name = Column(String, nullable=False)
    operation = Column(String, nullable=False)
    actor_uuid = Column(UUID(as_uuid=True), nullable=True)
    actor_role = Column(String, nullable=True)
    actor_ip = Column(String, nullable=True)
    row_id = Column(UUID(as_uuid=True), nullable=True)
    old_data = Column(JSON, nullable=True)
    new_data = Column(JSON, nullable=True)
    changed_fields = Column(ARRAY(String), nullable=True)
    session_id = Column(UUID(as_uuid=True), nullable=True)
    request_id = Column(String, nullable=True)
