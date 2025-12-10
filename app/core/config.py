from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    DATABASE_URL: str = Field(...)
    DB_USER: str = Field(..., min_length=1)
    DB_PASSWORD: str = Field(..., min_length=1)
    DB_NAME: str = Field(..., min_length=1)
    DB_HOST: str = Field(..., min_length=1)
    DB_PORT: str = Field(..., min_length=1)
    # CORS_ORIGINS: list[str] = Field(default=["http://localhost:5173"])
    SECRET_KEY: str = Field(...)
    ALGORITHM: str = Field(...)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)

    class Config:
        env_file = ".env"


settings = Settings()
