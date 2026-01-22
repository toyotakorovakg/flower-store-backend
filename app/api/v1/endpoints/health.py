# app/api/v1/endpoints/health.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.db.session import get_db

router = APIRouter()

@router.get("/", tags=["health"], summary="Проверка подключения к базе данных")
async def health_check(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """
    Пытается выполнить запрос SELECT 1. Если база недоступна, выбрасывается исключение.
    """
    try:
        await db.execute(text("SELECT 1"))
    except Exception as exc:
        # пробрасываем исключение как 500 Internal Server Error
        raise HTTPException(status_code=500, detail=f"Database connection error: {exc}")
    return {"status": "ok"}
