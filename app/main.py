"""
Entry point for the FastAPI application.

This module initializes and configures the app, including middleware,
exception handlers and API routers. It also wires up database connection
and ensures secure settings are loaded at startup.
"""

from __future__ import annotations

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.core.logging import setup_logging  # ensure logging is configured
from app.api.v1.endpoints import (
    auth as auth_endpoints,
    users as users_endpoints,
    orders as orders_endpoints,
    products as products_endpoints,
    support as support_endpoints,
    messages as messages_endpoints,
)


def create_app() -> FastAPI:
    """Create and configure a new FastAPI application instance."""
    setup_logging()
    app = FastAPI(
        title="Secure Flower Store API",
        version="1.0.0",
        description=(
            "Backend API for the Secure Flower Store. Implements strict "
            "authentication, authorization and secure data handling."
        ),
    )

    # CORS settings: adjust origins in production
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: restrict in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routers with version prefix
    from fastapi import APIRouter

    api_router = APIRouter()
    api_router.include_router(auth_endpoints.router, prefix="/auth", tags=["auth"])
    api_router.include_router(users_endpoints.router, prefix="/users", tags=["users"])
    api_router.include_router(orders_endpoints.router, prefix="/orders", tags=["orders"])
    api_router.include_router(products_endpoints.router, prefix="/products", tags=["products"])
    api_router.include_router(support_endpoints.router, prefix="/support", tags=["support"])
    api_router.include_router(messages_endpoints.router, prefix="/messages", tags=["messages"])

    app.include_router(api_router, prefix="/api/v1")

    @app.on_event("startup")
    async def startup_event() -> None:
        """Run tasks on application startup.

        This can include database connectivity checks and any initialisation
        required before serving requests.
        """
        # Attempt a database connection to fail fast if the DSN is invalid.
        from sqlalchemy import text
        from app.db.session import async_session

        async with async_session() as session:
            try:
                await session.execute(text("SELECT 1"))
            except Exception as exc:
                logging.exception("Database connection failed: %s", exc)
                raise

    return app


app = create_app()
