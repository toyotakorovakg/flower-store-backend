"""
Entry point for the FastAPI application.

This version of ``main.py`` retains the original structure of your
FlowerвЂ‘Store backend (importing routers for ``auth``, ``users``,
``orders``, ``products``, ``support`` and ``messages``) while adding a
root endpoint and including new healthвЂ‘check and databaseвЂ‘info
routers.  It also performs a simple database connectivity check on
startup.  Use this file to replace ``app/main.py`` in your project
after adding the corresponding ``health.py`` and ``dbinfo.py``
endpoints.
"""
from __future__ import annotations

import logging

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.core.logging import setup_logging

# Import existing endpoint modules
from app.api.v1.endpoints import (
    auth as auth_endpoints,
    users as users_endpoints,
    orders as orders_endpoints,
    products as products_endpoints,
    support as support_endpoints,
    messages as messages_endpoints,
    health as health_endpoints,
    dbinfo as dbinfo_endpoints,
)

from sqlalchemy import text
from app.db.session import async_session


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
    api_router = APIRouter()
    api_router.include_router(auth_endpoints.router, prefix="/auth", tags=["auth"])
    api_router.include_router(users_endpoints.router, prefix="/users", tags=["users"])
    api_router.include_router(orders_endpoints.router, prefix="/orders", tags=["orders"])
    api_router.include_router(products_endpoints.router, prefix="/products", tags=["products"])
    api_router.include_router(support_endpoints.router, prefix="/support", tags=["support"])
    api_router.include_router(messages_endpoints.router, prefix="/messages", tags=["messages"])
    api_router.include_router(health_endpoints.router, prefix="/health", tags=["health"])
    api_router.include_router(dbinfo_endpoints.router, prefix="/dbinfo", tags=["dbinfo"])

    app.include_router(api_router, prefix="/api/v1")

    @app.get("/", summary="Root endpoint", tags=["root"])
    async def read_root() -> dict[str, str]:
        """Return a welcome message and hints for users."""
        return {
            "message": "Welcome to the Flower Store API. See /api/v1/health for DB status or /docs for documentation."
        }

    @app.on_event("startup")
    async def startup_event() -> None:
        """Run tasks on application startup.

        Attempt a simple SELECT against the database to fail fast if the DSN
        is invalid.  If the query fails, log the exception and stop
        the application from starting.
        """
        async with async_session() as session:
            try:
                await session.execute(text("SELECT 1"))
                logging.info("Database connectivity check passed.")
            except Exception as exc:
                logging.exception("Database connection failed: %s", exc)
                raise

    return app


app = create_app()