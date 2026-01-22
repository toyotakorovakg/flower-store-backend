"""
Main entry point for the FastAPI application.

This module creates and configures a FastAPI instance, wires up
middleware, exception handlers and API routers, and performs a
database connectivity check on startup.  It also defines a simple
root endpoint and a demonstration endpoint to prove that the
application can talk to the database.

Replace your existing `app/main.py` with this file to adopt the
configuration described in the instructions.  The code assumes
environment variables are loaded via the Settings class in
``app/core/settings.py`` and that the asynchronous engine and session
are defined in ``app/db/session.py``.  For a working database
connection, ensure you have set ``DB_HOST``, ``DB_PORT``, ``DB_NAME``,
``DB_USER`` and ``DB_PASSWORD`` in your ``.env`` file (Supavisor
connection details for Supabase) and provided strong values for
``ENCRYPTION_KEY``, ``EMAIL_PEPPER`` and ``JWT_SECRET_KEY``.
"""
from __future__ import annotations

import logging

from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.db.session import async_session

# Import your API routers.  You can add new routers (such as a
# health check or database info router) by including them here and
# registering them on the ``api_router`` below.
from app.api.v1.endpoints import (
    products as products_endpoints,
    support as support_endpoints,
    messages as messages_endpoints,
    health as health_endpoints,
    dbinfo as dbinfo_endpoints,
)


def create_app() -> FastAPI:
    """Create and configure a new FastAPI application instance."""
    # Initialise logging as early as possible.
    logging.basicConfig(level=logging.INFO)

    app = FastAPI(
        title="Flower Store API",
        version="1.0.0",
        description=(
            "Backend API for the Flower Store. Provides endpoints for products,"
            " orders, users and support messages, and includes a health check"
            " to verify database connectivity."
        ),
    )

    # CORS settings: adjust ``allow_origins`` in production to restrict
    # clients.  During development we allow everything for convenience.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Create a versioned API router and register endpoint modules.
    api_router = APIRouter()
    api_router.include_router(products_endpoints.router, prefix="/products", tags=["products"])
    api_router.include_router(support_endpoints.router, prefix="/support", tags=["support"])
    api_router.include_router(messages_endpoints.router, prefix="/messages", tags=["messages"])
    api_router.include_router(health_endpoints.router, prefix="/health", tags=["health"])
    api_router.include_router(dbinfo_endpoints.router, prefix="/dbinfo", tags=["dbinfo"])

    # Mount the versioned API under /api/v1
    app.include_router(api_router, prefix="/api/v1")

    # Define a root endpoint so that hitting the base URL returns a
    # helpful message instead of 404.  This endpoint does not access
    # the database.
    @app.get("/", summary="Root endpoint", tags=["root"])
    async def read_root() -> dict[str, str]:
        return {
            "message": "Welcome to the Flower Store API. Visit /api/v1/health to check the database or /docs for documentation."
        }

    # Health check on startup: attempt to connect to the database to fail
    # fast if the DSN is misconfigured.  This uses the same ``async_session``
    # dependency as the API endpoints.
    @app.on_event("startup")
    async def startup_event() -> None:
        """Run tasks on application startup.

        Try executing a simple SELECT to verify the database is reachable.
        If the connection fails, log the exception and re-raise it to
        prevent the app from starting.
        """
        async with async_session() as session:
            try:
                await session.execute(text("SELECT 1"))
                logging.info("Database connectivity check passed.")
            except Exception as exc:
                logging.exception("Database connection failed: %s", exc)
                # Stop the app from starting if the DB connection fails
                raise

    return app


# Create a global app instance for use with Uvicorn or other ASGI servers.
app = create_app()