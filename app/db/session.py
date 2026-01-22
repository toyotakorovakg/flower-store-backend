"""
Asynchronous SQLAlchemy session configuration with backwards-compatible
dependency names.

This version of the session module exposes both ``get_db`` and
``get_session``.  Many endpoint modules import ``get_session`` to
acquire an ``AsyncSession`` dependency; adding ``get_session`` as an alias
for ``get_db`` preserves compatibility with existing code while still
supporting the new configuration using Supabase's Supavisor pooler.
"""
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.settings import settings


def _create_engine():
    return create_async_engine(
        settings.dsn,
        echo=False,
        poolclass=NullPool,
        connect_args={
            "statement_cache_size": 0,
            "prepared_statement_cache_size": 0,
        },
    )


engine = _create_engine()
async_session: sessionmaker[AsyncSession] = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncSession:
    """Yield a new ``AsyncSession`` for dependency injection."""
    async with async_session() as session:
        yield session


# Backwards-compatible alias used by existing endpoints
async def get_session() -> AsyncSession:
    """Alias for get_db to maintain compatibility with existing imports."""
    async with async_session() as session:
        yield session