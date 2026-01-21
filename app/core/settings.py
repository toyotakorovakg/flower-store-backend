from __future__ import annotations

import functools
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """
    Глобальные настройки приложения, загружаемые из переменных окружения или файла .env.

    Для безопасности секреты и учетные данные должны предоставляться через переменные окружения или менеджер секретов.
    При использовании URL базы данных (например, от Supabase) задайте переменную ``DATABASE_URL`` и оставьте ``DB_*`` пустыми.

    Эта версия адаптирована под Pydantic v2: имена переменных окружения сопоставляются полям через `validation_alias`, что
    позволяет использовать привычные верхне‑регистрированные названия (DATABASE_URL, DB_HOST и т. п.) при сохранении
    питоновских имён полей. Лишние переменные окружения игнорируются.
    """

    # Параметры подключения к базе данных
    database_url: Optional[str] = Field(None, validation_alias="DATABASE_URL")
    db_host: Optional[str] = Field(None, validation_alias="DB_HOST")
    db_port: Optional[int] = Field(None, validation_alias="DB_PORT")
    db_name: Optional[str] = Field(None, validation_alias="DB_NAME")
    db_user: Optional[str] = Field(None, validation_alias="DB_USER")
    db_password: Optional[str] = Field(None, validation_alias="DB_PASSWORD")

    # Шифрование и безопасность
    encryption_key: str = Field(..., validation_alias="ENCRYPTION_KEY", min_length=32)
    email_pepper: str = Field(..., validation_alias="EMAIL_PEPPER", min_length=16)
    jwt_secret_key: str = Field(..., validation_alias="JWT_SECRET_KEY", min_length=32)

    # Конфигурация SettingsConfigDict: загружать .env, игнорировать лишние переменные и не учитывать регистр
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    def dsn(self) -> str:
        """Return the SQLAlchemy DSN string for the database.

        If a full ``DATABASE_URL`` is provided it is returned after ensuring
        it uses the asyncpg driver.  Otherwise construct a PostgreSQL DSN
        using the individual ``DB_*`` settings.  A ValueError is raised if
        insufficient pieces are provided.
        """
        if self.database_url:
            url = self.database_url
            # Заменяем протокол на asyncpg, если задано синхронное соединение
            if url.startswith("postgresql://"):
                url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
            return url
        host = self.db_host
        port = self.db_port
        name = self.db_name
        user = self.db_user
        password = self.db_password
        if not all([host, port, name, user, password]):
            raise ValueError(
                "Either DATABASE_URL or all of DB_HOST, DB_PORT, DB_NAME, "
                "DB_USER and DB_PASSWORD must be provided"
            )
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"


@functools.lru_cache()
def get_settings() -> Settings:
    """Возвращает кешированный экземпляр Settings."""
    return Settings()


settings: Settings = get_settings()
