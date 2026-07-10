from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://msme:msme@localhost:5432/msme"
    telegram_token: str = ""

    model_config = {"env_file": ".env"}


settings = Settings()
