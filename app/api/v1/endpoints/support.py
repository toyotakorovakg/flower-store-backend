"""
Support staff endpoints.

Support staff have special permissions to manage orders and messages. These
endpoints require role checks.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.get("/dashboard", summary="Support dashboard")
async def dashboard() -> dict:
    """Return metrics or tasks for support staff.

    This is a stub. Replace with real implementation.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Support dashboard not implemented yet",
    )
