"""
Pydantic schemas for user representations.
"""

from pydantic import BaseModel


class User(BaseModel):
    id: str
    role: str
    full_name: str | None = None
    is_active: bool
    exists: bool

    class Config:
        orm_mode = True
