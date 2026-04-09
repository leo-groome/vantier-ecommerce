"""Global application settings loaded from environment variables."""

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration sourced from .env file.

    All values are required unless a default is provided. Sensitive values
    (secrets, API keys) must never be committed to version control.
    """

    # Database
    database_url: str

    # Neon Auth
    neon_auth_jwks_url: str
    neon_auth_audience: str

    # Stripe
    stripe_secret_key: str
    stripe_webhook_secret: str

    # envia.com
    envia_api_key: str
    envia_base_url: str = "https://api.envia.com"

    # Resend
    resend_api_key: str
    resend_from_email: str = "noreply@vantier.com"
    resend_support_email: str = "luxury@vantiersupport.com"

    # Storage
    storage_url: str

    # App
    environment: str = "development"
    cors_origins: list[str] = ["http://localhost:5173"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors(cls, v: str | list[str]) -> list[str]:
        """Accept JSON array or comma-separated string from env."""
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    """Return cached Settings instance (loaded once at startup)."""
    return Settings()
