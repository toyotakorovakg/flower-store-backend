"""
SQLAlchemy model for chat messages.

Messages are exchanged between clients, support staff and AI bots. Each
message belongs to a conversation (session) and is associated with either
a customer or support staff member. Encryption of sensitive content should
be handled at the service layer.
"""

from __future__ import annotations

import uuid
from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    JSON,
    func,
)
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


class Message(Base):
    """Represents a chat message in the system."""

    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), nullable=False)
    client_id = Column(UUID(as_uuid=True), nullable=True)
    support_id = Column(UUID(as_uuid=True), nullable=True)
    content = Column(String, nullable=False)
    chat_type = Column(String, nullable=False, server_default="ai_bot")
    is_from_client = Column(Boolean, nullable=False, server_default="true")
    is_read = Column(Boolean, nullable=False, server_default="false")
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
