from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings are read from environment variables (or from a .env file)."""

    database_url: str = "postgresql+psycopg://registry:registry@localhost:5432/registry"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
