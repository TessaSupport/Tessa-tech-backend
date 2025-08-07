from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./terra.db"

    API_PREFIX: str = "/api"

    # DEBUG: bool = False

    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    SECRET_KEY: str

    ALGORITHM: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> List[str]:
        return [origin.strip() for origin in v.split(",")] if v else []

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()