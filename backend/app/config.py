from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    app_name: str = "Portfolio API"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    # Database settings
    database_url: str = "sqlite:///./data/portfolio.db"

    # Authentication settings
    admin_token: str = ""  # Simple admin token for OWNER access

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


# Ensure data directory exists
def ensure_data_dir():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir
