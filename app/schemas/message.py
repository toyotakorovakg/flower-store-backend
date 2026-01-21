"""
Pydantic schemas for message data.

This schema defines the fields returned for chat messages.  The
``model_config`` attribute enables Pydantic v2 to read data from ORM
objects when validating.
"""

from pydantic import BaseModel, ConfigDict


class MessageOut(BaseModel):
    id: str
    session_id: str
    client_id: str | None
    support_id: str | None
    content: str
    chat_type: str
    is_from_client: bool
    is_read: bool
    metadata: dict | None

    model_config = ConfigDict(from_attributes=True)
