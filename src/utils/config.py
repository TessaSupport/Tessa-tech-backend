import os
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Optional
from dotenv import load_dotenv

ENV = os.getenv("ENV", "dev") 

env_path = os.path.join(os.getcwd(), '..', f'.env.{ENV}')
load_dotenv(env_path)


class Settings(BaseSettings):
    ENV: str = ENV
    DATABASE_URL: str = "sqlite:///./tessa.db"
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    SECRET_KEY: str
    ALGORITHM: str 
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Email settings - make optional for development
    POSTMARK_API_TOKEN: Optional[str] = None
    DEFAULT_FROM_EMAIL: Optional[str] = None


    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> List[str]:
        return [origin.strip() for origin in v.split(",")] if v else []

    class Config:
        env_file = f".env.{ENV}"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()