from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "TODO List API"
    debug: bool = False

    database_url: str = "sqlite+aiosqlite:///./todo.db"
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    cors_origins: list[str] = ["http://localhost:4200"]

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
