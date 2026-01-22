"""
Updated Settings module compatible with Pydantic 1.x and 2.x.

Pydantic v2 moved the ``BaseSettings`` class into a separate package
(`pydantic-settings`), which can cause import errors on older code.
This module tries to import ``BaseSettings`` from ``pydantic_settings``
and falls back to importing from ``pydantic`` if necessary.  It also
defines a ``Settings`` class for loading environment variables and
constructing a PostgreSQL DSN from individual database parameters.
"""
from __future__ import annotations

from functools import lru_cache

try:
    # Pydantic >=2.0: BaseSettings is in pydantic-settings package
    from pydantic_settings import BaseSettings
except ImportError:  # pragma: no cover
    # Pydantic <2.0: BaseSettings is in pydantic
    from pydantic import BaseSettings  # type: ignore

from pydantic import Field


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    db_host: str = Field(..., env="DB_HOST")
    db_port: int = Field(..., env="DB_PORT")
    db_name: str = Field(..., env="DB_NAME")
    db_user: str = Field(..., env="DB_USER")
    db_password: str = Field(..., env="DB_PASSWORD")

    encryption_key: str = Field(..., env="ENCRYPTION_KEY")
    email_pepper: str = Field(..., env="EMAIL_PEPPER")
    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")

    @property
    def dsn(self) -> str:
        """Return an asyncpg-compatible DSN composed from component parts."""
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()


# Create a module-level settings instance
settings = get_settings()