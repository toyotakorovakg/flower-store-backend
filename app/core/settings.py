"""
Application configuration using Pydantic for strict validation.

This module loads configuration from environment variables or an `.env` file
and exposes a single `settings` instance used throughout the application.
Sensitive values (like database credentials and encryption keys) must never
be hard‑coded; instead they should be provided via environment variables.

This version has been updated for Pydantic v2.  In Pydantic 2 the
`BaseSettings` class has moved to the `pydantic‑settings` package and
validators are implemented differently.  To avoid relying on deprecated
features we construct the database DSN lazily in the `dsn()` method rather
than using a validator to populate the `database_url` field.
"""

from __future__ import annotations

import functools
from typing import Optional

# Note: BaseSettings is provided by the separate `pydantic-settings` package in
# Pydantic v2.  It handles reading environment variables and `.env` files.
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Global application settings loaded from environment variables.

    It is critical for security that secrets and credentials are injected via
    environment variables or a secrets manager; do not commit real values into
    source control.  When using a database URL (e.g. provided by Supabase)
    set ``DATABASE_URL`` and leave individual ``DB_*`` fields unset.
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
        # Tell pydantic where to load environment variables from and to treat
        # variable names as case sensitive.
        env_file = ".env"
        case_sensitive = True

    def dsn(self) -> str:
        """Return the SQLAlchemy DSN string for the database.

        If a full ``DATABASE_URL`` is provided it is returned verbatim.
        Otherwise construct a PostgreSQL DSN using the individual ``DB_*``
        settings.  A ValueError is raised if insufficient pieces are provided.
        """
        if self.database_url:
            return self.database_url
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
    """Return a cached settings instance to avoid repeated parsing."""
    return Settings()


# Export a module‑level settings instance for convenience.  Importing this
# variable will trigger loading of environment variables once and then reuse
# the cached instance for subsequent imports.
settings: Settings = get_settings()
