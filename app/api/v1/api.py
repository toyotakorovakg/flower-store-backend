"""
Versioned API router for v1 endpoints.

This version of the API router includes the existing endpoint modules
(`products`, `support`, `messages`) as well as new modules `health`
and `dbinfo` that provide database health checks and demonstration
queries.
"""
from fastapi import APIRouter

from .endpoints import products, support, messages, health, dbinfo

api_router = APIRouter()
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(support.router, prefix="/support", tags=["support"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(dbinfo.router, prefix="/dbinfo", tags=["dbinfo"])