"""
Application settings using Pydantic.

This module defines a `Settings` class for loading configuration from
environment variables or a `.env` file.  It assembles a PostgreSQL DSN
from individual variables (DB_HOST, DB_PORT, DB_NAME, DB_USER,
DB_PASSWORD) rather than relying on a single `DATABASE_URL`.  This
approach is compatible with Supabase's Supavisor pooler, which uses a
specialised hostname and port.
"""
from __future__ import annotations

from functools import lru_cache
from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    # Database connection parameters
    db_host: str = Field(..., env="DB_HOST")
    db_port: int = Field(..., env="DB_PORT")
    db_name: str = Field(..., env="DB_NAME")
    db_user: str = Field(..., env="DB_USER")
    db_password: str = Field(..., env="DB_PASSWORD")

    # Secrets for encryption, email peppering and JWTs.  Replace these
    # placeholders with secure random strings in your `.env`.
    encryption_key: str = Field(..., env="ENCRYPTION_KEY")
    email_pepper: str = Field(..., env="EMAIL_PEPPER")
    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")

    @property
    def dsn(self) -> str:
        """Construct an asyncpg-compatible DSN from component parts."""
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    # Optionally perform validation on secrets lengths
    @validator("encryption_key")
    def encryption_key_must_be_hex(cls, v: str) -> str:  # noqa: N805
        if len(v) < 64:
            raise ValueError("ENCRYPTION_KEY must be at least 32 bytes encoded as hex (64 characters)")
        return v

    @validator("email_pepper")
    def email_pepper_must_be_hex(cls, v: str) -> str:  # noqa: N805
        if len(v) < 32:
            raise ValueError("EMAIL_PEPPER must be at least 16 bytes encoded as hex (32 characters)")
        return v

    @validator("jwt_secret_key")
    def jwt_secret_key_must_be_hex(cls, v: str) -> str:  # noqa: N805
        if len(v) < 64:
            raise ValueError("JWT_SECRET_KEY must be at least 32 bytes encoded as hex (64 characters)")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Return a cached instance of Settings to avoid re-reading the environment."""
    return Settings()


# Instantiate the settings at import time for convenience.
settings: Settings = get_settings()