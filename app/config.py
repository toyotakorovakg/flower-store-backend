from pydantic import BaseSettings, Field


class Config(BaseSettings):
    db_host: str = Field(..., env="DB_HOST")
    db_port: int = Field(..., env="DB_PORT")
    db_name: str = Field(..., env="DB_NAME")
    db_user: str = Field(..., env="DB_USER")
    db_password: str = Field(..., env="DB_PASSWORD")

    # РЎРµРєСЂРµС‚РЅС‹Рµ РєР»СЋС‡Рё
    encryption_key: str = Field(..., env="ENCRYPTION_KEY")
    email_pepper: str = Field(..., env="EMAIL_PEPPER")
    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def database_dsn(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

config = Config()