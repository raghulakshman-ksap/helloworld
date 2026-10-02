from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "helloworld-api"
    # Origins allowed to call the API from a browser (the Next.js dev server by default).
    cors_origins: list[str] = ["http://localhost:3000"]

    model_config = SettingsConfigDict(env_file=".env", env_prefix="API_")


settings = Settings()
