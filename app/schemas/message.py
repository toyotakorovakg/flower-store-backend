"""
Pydantic schemas for message data.

This schema defines the fields returned for chat messages.  The
``model_config`` attribute enables Pydantic v2 to read data from ORM
objects when validating.  We alias the ``metadata_json`` attribute from
the model to the ``metadata`` field in the API response.
"""

from pydantic import BaseModel, ConfigDict, Field


class MessageOut(BaseModel):
    id: str
    session_id: str
    client_id: str | None
    support_id: str | None
    content: str
    chat_type: str
    is_from_client: bool
    is_read: bool
    # В модели поле называется metadata_json, но пользователям API
    # это поле по‑прежнему возвращается как «metadata».
    metadata: dict | None = Field(None, alias="metadata_json")

    # Параметр populate_by_name позволяет обращаться к полю «metadata_json» как к «metadata»
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
