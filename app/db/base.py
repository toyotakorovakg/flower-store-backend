"""
Base declarative class for SQLAlchemy models.

All ORM models in the application should inherit from `Base` to ensure they
share the same metadata.  This file does not define any models by itself,
but importing it ensures that model metadata can be collected for things
like migrations.
"""
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """Custom declarative base that automatically generates table names."""

    @declared_attr.directive
    def __tablename__(cls) -> str:  # type: ignore[override]
        return cls.__name__.lower()
