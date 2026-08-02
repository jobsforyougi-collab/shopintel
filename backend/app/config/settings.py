from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    # ---------------------------------------------------------
    # Application
    # ---------------------------------------------------------
    app_name: str
    app_version: str
    debug: bool

    # ---------------------------------------------------------
    # Database
    # ---------------------------------------------------------
    database_url: str

    # ---------------------------------------------------------
    # Security
    # ---------------------------------------------------------
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # ---------------------------------------------------------
    # Environment File
    # ---------------------------------------------------------
    model_config = SettingsConfigDict(
    env_file=".env.development",
    env_file_encoding="utf-8",
    case_sensitive=False,
    extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.

    The settings are loaded only once during application startup.
    """
    return Settings()


settings = get_settings()