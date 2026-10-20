"""Environment-backed settings for the API."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "crypto_dashboard"
    db_user: str = "postgres"
    db_password: str = ""
    db_sslmode: str = "prefer"

    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()
