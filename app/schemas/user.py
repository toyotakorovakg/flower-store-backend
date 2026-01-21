"""
Pydantic schemas for user representations.

This version uses Pydantic v2's configuration style.  The ``model_config``
attribute is set so that Pydantic will read attributes from SQLAlchemy ORM
objects when validating, replacing the deprecated ``orm_mode`` option.
"""

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    id: str
    role: str
    full_name: str | None = None
    is_active: bool
    exists: bool

    # Enable reading attributes from ORM objects.  See
    # https://docs.pydantic.dev/latest/usage/models/#from-attributes-and-arbitrary-class-instances
    model_config = ConfigDict(from_attributes=True)
