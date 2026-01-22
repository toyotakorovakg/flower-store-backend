"""
Endpoint for health checks.

This module exposes a simple GET endpoint that attempts to execute a
lightweight SQL statement against the database.  If the query
succeeds, the endpoint responds with ``{"status": "ok"}``.  If it
fails, a 500 error is returned with details of the exception.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db


router = APIRouter()


@router.get("/", summary="Health check", response_model=dict)
async def health_check(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """Verify that the database connection is alive.

    Tries to execute ``SELECT 1`` using the provided ``db`` session.
    If any exception occurs, return a 500 error with details.
    """
    try:
        await db.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database connection error: {exc}") from exc
    return {"status": "ok"}