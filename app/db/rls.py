"""
Utilities for setting row-level security (RLS) session variables.

These helper functions can be used to set PostgreSQL session variables that
control row-level security policies. They should be called at the start of
each request after authentication.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


async def set_rls_context(
    session: AsyncSession,
    actor_uuid: str,
    actor_role: str,
    client_id: str | None = None,
) -> None:
    """Set RLS session variables for the current connection.

    Parameters
    ----------
    session:
        The SQLAlchemy AsyncSession whose connection will have the variables set.
    actor_uuid:
        UUID of the authenticated actor.
    actor_role:
        Role of the actor (e.g., 'customer', 'support', 'admin').
    client_id:
        Optional client ID associated with the actor (for customers).
    """
    vars_sql = (
        "SET app.actor_uuid = :actor_uuid, "
        "app.actor_role = :actor_role, "
        "app.client_id = :client_id"
    )
    await session.execute(
        text(vars_sql),
        {
            "actor_uuid": actor_uuid,
            "actor_role": actor_role,
            "client_id": client_id or "",
        },
    )
