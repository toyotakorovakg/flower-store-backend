# app/api/v1/api.py
from fastapi import APIRouter

from .endpoints import products, support, messages, health  # импортируем health

api_router = APIRouter()

api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(support.router, prefix="/support", tags=["support"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
api_router.include_router(health.router, prefix="/health", tags=["health"])  # новый эндпоинт
