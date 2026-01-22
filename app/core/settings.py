from __future__ import annotations
import functools
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    db_host: str = Field(..., validation_alias="DB_HOST")
    db_port: int = Field(..., validation_alias="DB_PORT")
    db_name: str = Field(..., validation_alias="DB_NAME")
    db_user: str = Field(..., validation_alias="DB_USER")
    db_password: str = Field(..., validation_alias="DB_PASSWORD")

    encryption_key: str = Field(..., validation_alias="ENCRYPTION_KEY", min_length=32)
    email_pepper: str = Field(..., validation_alias="EMAIL_PEPPER", min_length=16)
    jwt_secret_key: str = Field(..., validation_alias="JWT_SECRET_KEY", min_length=32)

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    def dsn(self) -> str:
        if not all([self.db_host, self.db_port, self.db_name, self.db_user, self.db_password]):
            raise ValueError(
                "All of DB_HOST, DB_PORT, DB_NAME, DB_USER and DB_PASSWORD must be provided"
            )
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


@functools.lru_cache()
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()