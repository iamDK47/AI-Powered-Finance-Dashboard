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

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 720

    admin_username: str
    admin_password_hash: str

    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()
