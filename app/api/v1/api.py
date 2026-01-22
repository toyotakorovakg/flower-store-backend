"""
Versioned API router for v1 endpoints.

This module creates a top-level `APIRouter` and includes routers from
individual endpoint modules.  New endpoints can be added by
importing and including their routers here.
"""
from fastapi import APIRouter

from .endpoints import products, support, messages, health, dbinfo

# The API router for version 1.  Each endpoint module defines its own
# router, which is mounted under a specific prefix.  The tags help
# organise the Swagger documentation.
api_router = APIRouter()

api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(support.router, prefix="/support", tags=["support"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(dbinfo.router, prefix="/dbinfo", tags=["dbinfo"])