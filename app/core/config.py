from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "Travel Planner API"
    PROJECT_DESCRIPTION: str = "API for managing travel projects and places"

    # Database
    DATABASE_URL: str = "sqlite:///./travel_planner.db"

    # Art Institute API
    ART_API_BASE_URL: str = "https://api.artic.edu/api/v1/artworks"

    # Rate Limiting
    DEFAULT_RATE_LIMIT: str = "60/minute"

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3000/",
    ]

    # Trusted Hosts
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
