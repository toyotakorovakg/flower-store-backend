"""
Application configuration definitions.

This module defines a Config class that reads configuration values from environment
variables using Pydantic. It complements the settings module in core by providing
structured access to environment variables. Use this for database and secret keys.
"""

from pydantic import BaseSettings, Field


class Config(BaseSettings):
    """Configuration loaded from environment or .env file."""

    database_url: str = Field(..., env="DATABASE_URL")
    encryption_key: str = Field(..., env="ENCRYPTION_KEY")
    email_pepper: str = Field(..., env="EMAIL_PEPPER")
    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")

    class Config:
        env_file = ".env"
        case_sensitive = True


config = Config()
