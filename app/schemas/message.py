"""
    Pydantic schemas for message data.

    Defines the response model (MessageOut) and the request model (MessageCreate).
    When creating a message, use MessageCreate; when returning a message, use
    MessageOut.  The 'metadata_json' field in the ORM model is mapped to
    'metadata' in the API responses.
"""
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class MessageCreate(BaseModel):
    """Schema for creating a new chat message."""

    session_id: UUID
    client_id: Optional[UUID] = None
    support_id: Optional[UUID] = None
    content: str
    chat_type: str = "ai_bot"
    is_from_client: bool = True
    # Accept metadata as a dict; this will be saved to metadata_json in the DB
    metadata: Optional[dict] = None


class MessageOut(BaseModel):
    id: str
    session_id: str
    client_id: str | None
    support_id: str | None
    content: str
    chat_type: str
    is_from_client: bool
    is_read: bool
    # В модели поле называется metadata_json, но пользователям API это поле
    # по‑прежнему возвращается как «metadata».
    metadata: dict | None = Field(None, alias="metadata_json")

    # Параметр populate_by_name позволяет обращаться к полю «metadata_json» как к «metadata»
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
