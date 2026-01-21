"""
Database session utilities.

Defines the SQLAlchemy async engine and session factory configured from
application settings. Provides dependency helpers for FastAPI routes.
"""

from __future__ import annotations

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.settings import settings

# Create the async engine using the DSN from configuration.  `pool_pre_ping`
# helps detect and recycle dead connections, improving reliability. The
# `future=True` flag enables 2.x style usage.
engine = create_async_engine(
    settings.dsn(),
    pool_pre_ping=True,
    future=True,
)

# Create a sessionmaker factory bound to our engine. expire_on_commit=False
# prevents SQLAlchemy from expiring objects upon commit, which can help when
# returning ORM objects from endpoints.
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a single SQLAlchemy AsyncSession.

    Designed to be used as a FastAPI dependency. Using a generator ensures
    that the session is automatically closed after the request is processed.
    """
    async with async_session() as session:
        yield session
