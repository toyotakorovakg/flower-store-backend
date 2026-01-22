"""
Asynchronous SQLAlchemy session and engine configuration.

This module creates an asynchronous database engine using SQLAlchemy and
provides a dependency for acquiring `AsyncSession` objects within
FastAPI endpoints.  It is tailored for use with Supabase via the
Supavisor session or transaction pooler and disables prepared
statement caching, which Supavisor does not supportгЂђ185306601028191вЂ L39-L41гЂ‘.

To configure the connection, set the following environment variables
in your `.env` file or system environment:

```
DB_HOST      # Hostname of the Supavisor pooler (aws-...pooler.supabase.com)
DB_PORT      # Port number of the Supavisor pooler (6543 for transaction pooler)
DB_NAME      # Database name (usually 'postgres')
DB_USER      # Database user (e.g. 'postgres.<project-ref>')
DB_PASSWORD  # Password for the user
```

You should also set `ENCRYPTION_KEY`, `EMAIL_PEPPER` and
`JWT_SECRET_KEY` to strong random values, but they are not used
directly in this module.
"""
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.settings import settings


def _create_engine():
    """Create and return an asynchronous SQLAlchemy engine.

    The engine is configured to use ``NullPool`` because Supabase's
    Supavisor pooler manages connections externally.  Prepared statement
    caching is disabled by passing ``statement_cache_size=0`` and
    ``prepared_statement_cache_size=0`` in ``connect_args``, as required
    for Supabase transaction poolerгЂђ185306601028191вЂ L39-L41гЂ‘.
    """
    return create_async_engine(
        settings.dsn,
        echo=False,
        poolclass=NullPool,
        # Disables prepared statements; required for Supavisor
        connect_args={
            "statement_cache_size": 0,
            "prepared_statement_cache_size": 0,
        },
    )


# Create a single engine instance.  It will be lazy-initialised when first
# used.  Using a module-level engine avoids recreating the engine on
# every request.
engine = _create_engine()

# Configure a sessionmaker to create AsyncSession objects bound to the
# engine.  ``expire_on_commit=False`` keeps objects accessible after
# commit.
async_session: sessionmaker[AsyncSession] = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    """FastAPI dependency that yields a new AsyncSession.

    Each request gets its own session, which is closed automatically
    after the request finishes.
    """
    async with async_session() as session:
        yield session