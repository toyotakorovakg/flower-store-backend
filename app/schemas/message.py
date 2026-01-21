"""
Pydantic schemas for message data.
"""

from pydantic import BaseModel


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

    class Config:
        orm_mode = True
