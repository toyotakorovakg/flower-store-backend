"""
SQLAlchemy model for the unified users view.

In PostgreSQL, the application defines a view ``users_view`` that unions
customers and support staff. This model maps to that view, allowing
queries to return a unified representation of both types of user. Note
that since this maps to a view rather than a table, it should be marked
as read-only and does not define a primary key constraint on the view.
"""

from __future__ import annotations

from sqlalchemy import Boolean, Column, DateTime, String

from app.db.base import Base


class User(Base):
    __tablename__ = "users_view"
    __table_args__ = {"info": {"read_only": True}}

    id = Column(String, primary_key=True)  # UUID stored as string
    role = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, nullable=False)
    exists = Column(Boolean, nullable=False)
