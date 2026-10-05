from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # --- Database ---
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "crypto_dashboard"
    db_user: str = "postgres"
    db_password: str = ""

    # --- Auth ---
    jwt_secret_key: str  # required, no default — app refuses to start without one
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 720  # 12 hours

    # Single-admin login for now, not a users table. You are the only user of
    # your own dashboard today, so a full signup/user system would be
    # complexity with no current payoff — this still uses the *real* pattern
    # (hashed password, signed token), just against one identity instead of
    # a table of them. See README for how to grow this into a users table
    # later without changing anything else in the app.
    admin_username: str
    admin_password_hash: str  # a bcrypt hash — never store the plaintext password

    # --- CORS ---
    # Defaults to the standard Next.js dev server port. Override via env
    # only once you deploy somewhere with a real domain.
    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()
