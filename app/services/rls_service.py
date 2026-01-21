"""
Row-level security service.

This service provides convenience functions for applying row-level security
context to a database session. It imports the underlying helper from
``app.db.rls``.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.rls import set_rls_context as _set_rls_context


async def apply_rls_context(
    session: AsyncSession,
    *,
    actor_uuid: str,
    actor_role: str,
    client_id: str | None = None,
) -> None:
    """Set the session variables used by RLS policies.

    This simply calls the lower-level function from ``app.db.rls``.
    """
    await _set_rls_context(session, actor_uuid=actor_uuid, actor_role=actor_role, client_id=client_id)
