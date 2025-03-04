from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Optional
import secrets
import os

load_dotenv(dotenv_path="app/.env")

db_username = os.getenv("DATABASE_USERNAME")
db_password = os.getenv("DATABASE_PASSWORD")
db_name = os.getenv("DATABASE_NAME")

# Check if the environment variables are loaded correctly
if not db_username or not db_password:
    raise ValueError(
        "DATABASE_USERNAME or DATABASE_PASSWORD not found in .env file")


class Settings(BaseSettings):
    """Configuration settings for the application."""
    DATABASE_URL: str = f"mysql+pymysql://{db_username}:{db_password}@localhost/{db_name}"
    """Database connection URL."""
    SECRET_KEY: str = secrets.token_hex(32)
    """Secret key for JWT encoding."""
    ALGORITHM: str = "HS256"
    """JWT algorithm."""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    """Access token expiration time in minutes."""

    class Config:
        """Configuration settings for the Settings class."""
        env_file = ".env"
        """Path to the .env file."""


settings = Settings()
