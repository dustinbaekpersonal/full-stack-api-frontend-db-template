"""Configurations to be used in backend app."""
import os

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Settings used across backend.

    Example:
        asyncpg_url: postgresql database url
    """

    asyncpg_url: PostgresDsn = os.getenv("DB_URL")
    ## TODO: Add authentication feature
    # jwt_algorithm: str = os.getenv("JWT_ALGORITHM")
    # jwt_expire: int = os.getenv("JWT_EXPIRE")


settings = Settings()
