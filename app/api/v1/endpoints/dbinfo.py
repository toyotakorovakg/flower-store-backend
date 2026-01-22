"""
Endpoint for demonstrating database queries.

This module provides a GET endpoint that returns basic information
about the connected PostgreSQL database.  It queries the
``information_schema.tables`` view to list the names of tables in the
public schema.  This is a simple way to prove that the backend can
run SQL queries against the database and return the results as JSON.

You can extend this endpoint or create additional ones to perform
custom queries.  Be careful to avoid SQL injection if you accept
parameters from the client; use parameterised queries and avoid
concatenating raw input into SQL strings.
"""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db


router = APIRouter()


@router.get("/tables", summary="List tables", response_model=List[dict])
async def list_tables(db: AsyncSession = Depends(get_db)) -> List[dict]:
    """Return a list of table names in the public schema.

    Executes a query against ``information_schema.tables`` to fetch
    table names and returns them as a list of objects.  If the query
    fails, raises an HTTP 500 error.
    """
    query = text(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name
        """
    )
    try:
        result = await db.execute(query)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database query error: {exc}") from exc
    # Convert the result to a list of dicts for JSON serialisation.
    table_names = [row._asdict() for row in result.all()]
    return table_names