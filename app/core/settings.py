"""
Application configuration using Pydantic for strict validation.

This module loads configuration from environment variables or an .env file
and exposes a single `settings` instance used throughout the application.
Sensitive values (like database credentials and encryption keys) must never
be hard‑coded; instead they should be provided via environment variables.
"""

from __future__ import annotations

import functools
from typing import Optional

from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    """Global application settings loaded from environment variables.

    It is critical for security that secrets and credentials are injected
    via environment variables or a secrets manager; do not commit real values
    into source control.  When using a database URL (e.g. provided by Supabase)
    set `DATABASE_URL` and leave individual DB_* fields unset.
    """

    # Database connection parameters
    database_url: Optional[str] = Field(None, env="DATABASE_URL")
    db_host: Optional[str] = Field(None, env="DB_HOST")
    db_port: Optional[int] = Field(None, env="DB_PORT")
    db_name: Optional[str] = Field(None, env="DB_NAME")
    db_user: Optional[str] = Field(None, env="DB_USER")
    db_password: Optional[str] = Field(None, env="DB_PASSWORD")

    # Encryption and security
    encryption_key: str = Field(..., env="ENCRYPTION_KEY", min_length=32)
    email_pepper: str = Field(..., env="EMAIL_PEPPER", min_length=16)
    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY", min_length=32)

    class Config:
        env_file = ".env"
        case_sensitive = True

    @validator("database_url", always=True)
    def build_database_url(cls, v: Optional[str], values: dict) -> str:
        """Build a PostgreSQL connection string if `DATABASE_URL` isn't provided.

        Returns a DSN suitable for SQLAlchemy async engines using asyncpg.
        """
        if v:
            # If the user provides a full database URL we simply return it.
            return v

        host = values.get("db_host")
        port = values.get("db_port")
        name = values.get("db_name")
        user = values.get("db_user")
        password = values.get("db_password")
        if not all([host, port, name, user, password]):
            raise ValueError(
                "Either DATABASE_URL or all of DB_HOST, DB_PORT, DB_NAME, "
                "DB_USER and DB_PASSWORD must be provided"
            )
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"

    def dsn(self) -> str:
        """Return the SQLAlchemy DSN string for the database."""
        return self.database_url


@functools.lru_cache()
def get_settings() -> Settings:
    """Return a cached settings instance to avoid repeated parsing."""
    return Settings()


settings: Settings = get_settings()
